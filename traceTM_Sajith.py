import csv
import sys
import os


def ntm_bfs(ntm, tape, depth_limit):
    configs = [[["", ntm['start'], tape]]]
    level, index, end, end_type = 0, 0, False, ''
    
    while not end:
        curr = configs[level][index]

        if curr[1] == ntm['accept']:
            end_type = 'accepted'
            break

        if len(configs) == level + 1:
            configs.append([])

        if curr[1] != ntm['reject']:
            transition_made = False
            for next in ntm[curr[1]]:
                if next[0] == curr[2][0]:
                    transition_made = True
                    if next[3] == 'R':
                        if not curr[2][1:]:
                            configs[level + 1].append([curr[0] + next[2], next[1], '_'])
                        else:
                            configs[level + 1].append([curr[0] + next[2], next[1], curr[2][1:]])
                    elif next[3] == 'L':
                        if not curr[2][1:]:
                            configs[level + 1].append([curr[0][:-1], next[1], curr[0][-1] + next[2]])
                        else:
                            configs[level + 1].append([curr[0][:-1], next[1], curr[0][-1] + next[2] + curr[2][1:]])

            if not transition_made:
                configs[level + 1].append([curr[0], ntm['reject'], curr[2]])

        index += 1
        if index > len(configs[level]) - 1:
            end, end_type = True, 'rejected'
            for c in configs[level]:
                if c[1] != ntm['reject']:
                    end, end_type = False, ''
                    break
            if not configs[level + 1]:
                end = True
            level += 1
            index = 0
            if level > depth_limit:
                end_type = 'limit'
                end = True

    return configs, end_type

def simulate_ntm(tape, file_name, depth_limit):
    ntm = {}
    with open(f'data/{file_name}', mode='r', encoding='utf-8-sig') as file:
        csv_reader = csv.reader(file)
        for i, v in enumerate(csv_reader):
            if i < 7:
                if i == 0: ntm['Name'] = v[0]
                elif i == 1: ntm['Q'] = v
                elif i == 2: ntm['Σ'] = v
                elif i == 3: ntm['Γ'] = v
                elif i == 4: ntm['start'] = v[0]
                elif i == 5: ntm['accept'] = v[0]
                elif i == 6: ntm['reject'] = v[0]
            else:
                if v[0] not in ntm:
                    ntm[v[0]] = []
                ntm[v[0]].append(v[1:])
    
    configs, end_type = ntm_bfs(ntm, tape, depth_limit)
    
    return configs, ntm, end_type 


def output(configs, ntm, tape, end_type, output_file):
    output_file.write(f"Machine Name: {ntm['Name']}\n")
    output_file.write(f"Initial String: {tape}\n")
    output_file.write(f"Tree Depth: {len(configs) - 1}\n")
    output_file.write(f"Total Transitions Simulated: {sum([len(x) for x in configs])}\n")
    output_file.write(f"Measured nondeterminism: {sum([len(x) for x in configs if x]) / len([x for x in configs if x])}\n")
    
    if end_type == 'accepted':
        output_file.write(f"String accepted in {len(configs) - 1}\n")
    elif end_type == 'rejected':
        output_file.write(f"String rejected in {len(configs) - 1}\n")
    elif end_type == 'limit':
        output_file.write(f"Execution stopped after {len(configs)}\n")
    
    for level in configs:
        output_file.write(' '.join(''.join(c) for c in level) + '\n')



def main():
    prev_file = "" # Used to keep track of count of test for each machine
    with open('test_cases.txt', 'r') as test_file: # Reads all the test cases and runs the NTM for each test case
        for line in test_file:
            tape, depth_limit, file_name = line.strip().split()
            if file_name.strip() != prev_file:
                count = 1
                prev_file = file_name.strip()

            input_file_path = file_name
        
            configs, ntm, end_type = simulate_ntm(tape, input_file_path, int(depth_limit))

            num_machine = file_name.split('_')[1]
            output_file_path = os.path.join('outputs', f'output_machine_{num_machine}_test-{count}_Sajith.txt')

            # Output to corresponding file for the current test case
            with open(output_file_path, 'w') as output_file:
                output(configs, ntm, tape, end_type, output_file)

            count += 1
if __name__ == '__main__':
    main()
