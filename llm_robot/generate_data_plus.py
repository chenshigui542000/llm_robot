import random
import json

A = {"向", "往"}
B = {"前", "后", "左", "右", "左前", "右前", "左后", "右后"}
C = {"方", "方向", "面", "边"}
D = {"移动", "行走", "走", "前进"}
E = set(range(1, 51))
F = {"米"}
G = {","}
H = {"再", "接着", "然后"}
I = {"左转", "右转"}
J = set(range(1, 361))
K = {"度"}


output = {}


def get_train_data(n):

    for i in range(n):
        s = ""
        m = random.randint(1, 5)

        for _ in range(m):
            r = random.random()
            s1 = ""

            if r < 0.5:
                r1 = random.random()
                if r1 < 0.5:
                    s1 += random.choice(list(A))
                s1 += random.choice(list(B))
                r2 = random.random()
                if r2 < 0.5:
                    s1 += random.choice(list(C))
                s1 += random.choice(list(D)) + str(random.choice(list(E))) + random.choice(list(F))
            else:
                r1 = random.random()
                if r1 < 0.5:
                    s1 += random.choice(list(A))
                s1 += random.choice(list(I))
                s1 += str(random.choice(list(J))) + random.choice(list(K))

            if s != "":
                r = random.random()
                if r < 0.5:
                    s += random.choice(list(G)) + random.choice(list(H)) + s1
                else:
                    s += random.choice(list(G)) + s1
            else:
                s += s1

        output[f"question{i}"] = s


    output_json = json.dumps(output, ensure_ascii=False, indent=4)
    return output_json
