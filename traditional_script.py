import os

VTR_CMD = "/home/lohithprapoorna/Desktop/vtr-verilog-to-routing/vtr_flow/scripts/run_vtr_task.py regression_tests/vtr_reg_basic/basic_timing"
TASK_DIR = "/home/lohithprapoorna/Desktop/vtr-verilog-to-routing/vtr_flow/tasks/regression_tests/vtr_reg_basic/basic_timing"


def extract_adp(parse_file):
    print("reached extraction script")

    my_file = open(parse_file, "r+")
    my_file.seek(0)

    cont = my_file.readlines()
    headings = cont[0]
    values = cont[1]

    hwords = []
    vwords = []

    j = ''
    for i in headings:
        if i != '\t':
            j = j + i
        if i == '\t':
            hwords.append(j)
            j = ''

    j = ''
    for i in values:
        if i != '\t':
            j = j + i
        if i == '\t':
            vwords.append(j)
            j = ''

    area = -1
    delay = 0

    for i in range(0, len(hwords)):
        if hwords[i] == 'logic_block_area_total':
            area = float(vwords[i])
            print(area)
        if hwords[i] == 'crit_path_total_sta_time':
            delay = float(vwords[i])
            print(delay)

    my_file.close()

    print(len(hwords))
    print(len(vwords))

    if area == -1 or delay == 0:
        raise RuntimeError("Failed to extract area or delay")

    return [area * delay,area,delay]  # same behavior as original


def get_latest_run_dir():
    runs = [d for d in os.listdir(TASK_DIR) if d.startswith("run")]
    runs.sort()
    return os.path.join(TASK_DIR, runs[-1])


def main():
    print("Running VTR...")
    status = os.system(VTR_CMD)

    if status != 0:
        print("VTR failed")
        return

    run_dir = get_latest_run_dir()
    parse_file = os.path.join(run_dir, "parse_results.txt")

    adp = extract_adp(parse_file)

    with open("boundtop_trad_output.txt", "w") as f:
        f.write(f"ADP (Area x Delay): {adp[0]}\n")
        f.write(f"Area :{adp[1]}\n")
        f.write(f"delay :{adp[2]}")

    print("VTR run successful")
    print(f"ADP = {adp[0]}")
    print("Written to spree_traditional_output.txt")


if __name__ == "__main__":
    main()
