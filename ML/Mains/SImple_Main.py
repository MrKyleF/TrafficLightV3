import os
import sys
sys.path.insert(1, os.getcwd())

from Envs.Intersections.TwoOneWay import Intersection
from ML.Networks.Simple_Network import Agent
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plot

def getStepReward(step):
    sqaure = step * step
    cube = sqaure * step
    return ((cube - sqaure - step + 1) / step)

if __name__ == '__main__':
    #tf.compat.v1.disable_eager_execution()
    env = Intersection([[3, 10, 1],[1, 10, 0]])
    lr = 0.001
    n_games = 1000
    agent = Agent(gamma=0.99, epsilon=1.0, lr=lr, 
                input_dims=env.observation_space.shape,
                n_actions=env.actions, mem_size=1000000, batch_size=64,
                epsilon_end=0.10)
    scores = []
    eps_history = []
    steps = []

    for i in range(n_games):
        done = False
        score = 0
        observation = env.reset()
        current_step = 0
        while not done:
            current_step += 1
            action = agent.choose_action(observation)
            observation_, reward, done = env.step(action)
            reward += getStepReward(current_step)
            score += reward
            agent.store_transition(observation, action, reward, observation_, done)
            observation = observation_
            agent.learn()
            if score < 0 and current_step > 10:
                done = True
        eps_history.append(agent.epsilon)
        scores.append(score)
        steps.append(current_step)

        avg_score = np.mean(scores[-100:])
        avg_step = np.mean(steps[-100:])
        print('episode: ', i, 'score %.2f' % score,
                'step %.2f' % current_step,
                'average_score %.2f' % avg_score,
                'average_step %.2f' % avg_step,
                'epsilon %.2f' % agent.epsilon)
    plot.plot([i for i in range(0, len(scores))], scores, color='red')
    plot.plot([i for i in range(0, len(steps))], steps, color='green')
    plot.show()