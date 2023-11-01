import numpy as np
import time
import random

def SIR1(beta, gamma, df,time):
    # 模型参数
    # time = 1
    # beta = 0.5  # 传染率
    # gamma = 0.001  # 恢复率
    total_timesteps = len(df['timestep'].unique())  # 总时间步骤

    # 初始化 SIR 模型状态
    individuals_i = list(df['i'].unique())  # 所有个体 i
    individuals_j = list(df['j'].unique())  # 所有个体 j

    # 合并所有个体，去除重复的标识
    individuals = list(set(individuals_i + individuals_j))
    contacts_at_timestep = df[df['timestep'] == time]
    non_repeating_i = contacts_at_timestep["i"].unique()
    non_repeating_j = contacts_at_timestep["j"].unique()
    # 合并非重复的数字到一个新列表
    unique_numbers = list(set(non_repeating_i) | set(non_repeating_j))
    infected_number = random.choice(unique_numbers)
    # 随机选择一个个体作为初始感染者
    # initial_infected = np.random.choice(individuals, size=1, replace=False)

    # 初始化个体状态字典
    individual_states = {individual: 'S' for individual in individuals}
    individual_states[infected_number] = 'I'  # 初始感染者
    # individual_states[1] = 'I'
    susceptible = [len(individuals) - 1]  # 初始时刻，除初始感染者外的所有个体都是易感者
    infected = [1]  # 初始时刻，一个个体处于感染状态
    recovered = [0]  # 初始时刻，没有个体处于康复状态

    # 模拟 SIR 模型在每个时间步骤的演化
    for timestep in range(time, total_timesteps):
        new_infected = 0
        new_recovered = 0

        # 计算每个时间步骤内的新感染者和新康复者
        contacts_at_timestep = df[df['timestep'] == timestep]
        for _, contact in contacts_at_timestep.iterrows():
            if individual_states[contact['i']] == 'I':
                # print('individual infected -1 ')
                # i 感染了 j
                if individual_states[contact['j']] == 'S' and np.random.rand() < beta:
                    new_infected += 1
                    individual_states[contact['j']] = 'I'
            elif individual_states[contact['i']] == 'S':
                # i 与 j 接触，可能被感染
                # print('individual infected -2')
                if individual_states[contact['j']] == 'I' and np.random.rand() < beta:
                    individual_states[contact['i']] = 'I'
                    new_infected += 1

        # 恢复
        for individual in individuals:
            if individual_states[individual] == 'I' and np.random.rand() < gamma:
                new_recovered += 1
                individual_states[individual] = 'R'

        # 更新 SIR 模型状态
        susceptible.append(max(susceptible[-1] - new_infected, 0))
        infected.append(max(infected[-1] + new_infected - new_recovered, 0))
        recovered.append(recovered[-1] + new_recovered)

    # 绘制 SIR 模型的状态演化图
    # plt.figure(figsize=(10, 6))
    # plt.plot(range(total_timesteps), susceptible, label='Susceptible')
    # plt.plot(range(total_timesteps), infected, label='Infected')
    # plt.plot(range(total_timesteps), recovered, label='Recovered')
    # plt.xlabel('Time')
    # plt.ylabel('Number of Individuals')
    # plt.title('SIR Model Simulation')
    # plt.legend()
    # plt.show()
    total_num = infected[-1] + recovered[-1]
    # print(susceptible)
    result = [individual_states, total_num, infected_number]
    return result
