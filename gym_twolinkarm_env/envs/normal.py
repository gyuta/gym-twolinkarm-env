import gym
from gym import spaces
from gym.utils import seeding
import numpy as np
import math
from os import path
from scipy.integrate import solve_ivp


class TwoLinkArmEnv(gym.Env):
    metadata = {"render.modes": ["human", "rgb_array"], "video.frames_per_second": 30}

    def __init__(self):
        self.target = [1,1]

        self.physics = {
            "m1": 1.0,
            "m2": 1.0,

            "l1": 1.0,
            "l2": 1.0,
            "lg1": 0.5,
            "lg2": 0.5,

            "I1": 1/12,
            "I2": 1/12,

            "g": 0
        }

        self.config = {
            "t_span": [0, 0.05],
            "t_sample": np.linspace(0, 0.05, 10),
        }

        self.viewer = None

        o_high = np.array([np.pi, np.pi, np.finfo(np.float32).max, np.finfo(np.float32).max], dtype=np.float32)
        self.observation_space = spaces.Box(low=-o_high, high=o_high, dtype=np.float32)

        a_high = np.array([1.0, 1.0])
        self.action_space = spaces.Box(low=-a_high, high=a_high, dtype=np.float32)

        self.seed()

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def _model(self, t, y, tau):
        theta = y[:2]
        theta_dot = y[2:]

        M = self._calc_M(theta)
        M_inv = np.linalg.inv(M)
        h = self._calc_h(theta, theta_dot)
        g = self._calc_g(theta)

        theta_2dot = ( tau - h - g ) @ M_inv
        return np.concatenate((theta_dot,theta_2dot))
    
    def _calc_M(self, theta):
        p = self.physics

        a = p["m1"] * p["lg1"] ** 2 + p["I1"] + p["m2"] * (p["l1"] ** 2 + p["lg2"] ** 2 + 2 * p["l1"] * p["lg2"] * np.cos(theta[1]) + p["I2"])
        b = p["m2"] * (p["lg2"] ** 2 + p["l1"] * p["lg2"] * np.cos(theta[1])) + p["I2"]
        c = p["m2"] * p["lg2"] ** 2 + p["I2"]

        return np.array([[a,b], [b,c]])

    def _calc_h(self, theta, theta_dot):
        p = self.physics

        a = -p["m2"] * p["l1"] * p["lg2"] * np.sin(theta[1]) * (2 * theta_dot[0] * theta_dot[1] + theta_dot[1] ** 2)
        b =  p["m2"] * p["l1"] * p["lg2"] * np.sin(theta[1]) * theta_dot[0] ** 2

        return np.array([a,b])

    def _calc_g(self, theta):
        p = self.physics

        a = p["m1"] * p["g"] * p["lg1"] * np.cos(theta[0]) + p["m2"] * p["g"] * (p["l1"] * np.cos(theta[0] + p["lg2"] * np.cos(theta[0] + theta[1])))
        b = p["m2"] * p["g"] * p["lg2"] * np.cos(theta[0] + theta[1])

        return np.array([a,b])

    def step(self, u):
        res = solve_ivp(self._model, self.config["t_span"], self.state, method='LSODA',
                        t_eval=self.config["t_sample"], args=(u, ))

        self.state = res.y[:, -1].astype(np.float32)

        self.last_u = u
        
        
        self.step_cnt += 1
        done = self.step_cnt >= 200
        
        return self.state, self._get_reward(), done, {}
    
    def _get_reward(self):
        coord = self._get_tip_coord()
        pos_reward = -np.sum((coord - self.target)**2)
        vel_reward = -(math.fabs(self.state[2]) + math.fabs(self.state[3]))
        
        # return pos_reward + vel_reward
        return pos_reward
    
    def _get_tip_coord(self):
        p = self.physics
        a = p["l1"] * np.cos(self.state[0]) + p["l2"] * np.cos(self.state[0] + self.state[1])
        b = p["l1"] * np.sin(self.state[0]) + p["l2"] * np.sin(self.state[0] + self.state[1])

        return np.array([a,b])


    def reset(self):
        self.step_cnt = 0
        high = np.array([np.pi, np.pi, 0.0, 0.0])
        self.state = self.np_random.uniform(low=-high, high=high).astype(np.float32)
        self.last_u = None
        return self.state

    def render(self, mode="human"):
        if self.viewer is None:
            from gym.envs.classic_control import rendering

            self.viewer = rendering.Viewer(500, 500)
            self.viewer.set_bounds(-2.2, 2.2, -2.2, 2.2)

            rod = rendering.make_capsule(1, 0.2)
            rod.set_color(0.8, 0.3, 0.3)
            self.pole_transform = rendering.Transform()
            rod.add_attr(self.pole_transform)
            self.viewer.add_geom(rod)

            axle = rendering.make_circle(0.05)
            axle.set_color(0, 0, 0)
            self.viewer.add_geom(axle)

            axle2 = rendering.make_circle(0.05)
            axle2.set_color(0.1,0.1,0.1)
            self.axle2_transform = rendering.Transform()
            axle2.add_attr(self.axle2_transform)

            rod2 = rendering.make_capsule(1, 0.2)
            rod2.set_color(0.8, 0.3, 0.3)
            self.pole2_transform = rendering.Transform()
            rod2.add_attr(self.pole2_transform)
            rod2.add_attr(self.axle2_transform)
            self.viewer.add_geom(rod2)

            self.viewer.add_geom(axle2)


            target = rendering.make_circle(0.1)
            target.set_color(0.9, 0.9, 0)
            self.target_transform = rendering.Transform()
            target.add_attr(self.target_transform)
            self.viewer.add_geom(target)

            fname = path.join(path.dirname(__file__), "assets/clockwise.png")
            self.img = rendering.Image(fname, 1.0, 1.0)
            self.imgtrans = rendering.Transform()
            self.img.add_attr(self.imgtrans)

            self.img2 = rendering.Image(fname, 1.0, 1.0)
            self.imgtrans2 = rendering.Transform()
            self.img2.add_attr(self.imgtrans2)
            self.img2.add_attr(self.axle2_transform)

        self.viewer.add_onetime(self.img)
        self.viewer.add_onetime(self.img2)

        theta = self.state[0]
        self.pole_transform.set_rotation(theta)


        theta2 = self.state[1] + theta
        self.pole2_transform.set_rotation(theta2)

        self.axle2_transform.set_translation(math.cos(theta), math.sin(theta))

        if self.last_u is not None:
            scale = 1
            self.imgtrans.scale = (-scale*self.last_u[0], scale*np.abs(self.last_u[0]))
            self.imgtrans2.scale = (-scale*self.last_u[1], scale*np.abs(self.last_u[1]))
        
        self.target_transform.set_translation(*self.target)

        return self.viewer.render(return_rgb_array=mode == "rgb_array")

    def close(self):
        if self.viewer:
            self.viewer.close()
            self.viewer = None