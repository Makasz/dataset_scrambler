import csv
import random
import click
from math import ceil


def swap_letters(text, first, second):
    text_l = list(text)
    text_l[first], text_l[second] = text_l[second], text_l[first]
    return ''.join(text_l)


def scramble(swap, percent, chance):
    chance = 100 - chance/100
    swap = swap/100
    source = '../datasets/dataset_m.csv'
    pairs = f'../datasets/pairs_{swap}.csv'
    dest = source.replace('.csv', f'_scrambled_{swap}.csv')
    with open(source, 'r', encoding='utf8') as source_f:
        with open(dest, 'w', encoding='utf8') as dest_f:
            with open(pairs, 'w', encoding='utf8') as pairs_f:
                csv_reader = csv.reader(source_f, delimiter=';')
                for line in csv_reader:
                    line.append('id')
                    dest_f.write(';'.join(line) + '\n')
                    break
                id = 0
                lines = []
                # Randomize order of rows
                for line in csv_reader:
                    lines.append(line)
                random.shuffle(lines)
                # Take x% of rows to duplicate
                for line in lines[:int(len(lines)*percent)]:
                    new_line = line.copy()

                    # Swap % of letters in name, surname, pesel, city, street
                    for i in range(ceil(len(new_line[0]) * swap)):
                        a, b = random.sample(range(0, len(new_line[0]) - 1), 2)
                        new_line[0] = swap_letters(new_line[0], a, b)
                    for i in range(ceil(len(new_line[1]) * swap)):
                        try:
                            a, b = random.sample(range(0, len(new_line[1]) - 1), 2)
                            new_line[1] = swap_letters(new_line[1], a, b)
                        except:
                            new_line[1] = swap_letters(new_line[1], 0, 1)
                    for i in range(ceil(len(new_line[2]) * swap)):
                        a, b = random.sample(range(0, len(new_line[2]) - 1), 2)
                        new_line[2] = swap_letters(new_line[2], a, b)
                    for i in range(ceil(len(new_line[5]) * swap)):
                        a, b = random.sample(range(0, len(new_line[5]) - 1), 2)
                        new_line[5] = swap_letters(new_line[5], a, b)
                    for i in range(ceil(len(new_line[6]) * swap)):
                        a, b = random.sample(range(0, len(new_line[6]) - 1), 2)
                        new_line[6] = swap_letters(new_line[6], a, b)
                    # Swap name and surname
                    if random.randint(0, 100) > chance:
                        new_line[0], new_line[1] = new_line[1], new_line[0]
                    # Swap city and street
                    if random.randint(0, 100) > chance:
                        new_line[5], new_line[6] = new_line[6], new_line[5]
                    # Remove PESEL
                    if random.randint(0, 100) > chance:
                        new_line[2] = ''
                    # Change home number
                    if random.randint(0, 100) > chance:
                        new_line[7] = str(int(new_line[7]) + random.randint(0, 10))
                    if random.randint(0, 100) > chance:
                        new_line[3] = str(int(new_line[3][:4]) + random.randint(0, 10)) + new_line[3][4:]
                    # Write original and new line to output file
                    new_line.append(str(id))
                    pairs_f.write(str(id) + ';' + str(id + 1) + '\n')
                    dest_f.write(';'.join(new_line) + '\n')
                    id += 1
                    line.append(str(id))
                    id += 1
                    dest_f.write(';'.join(line) + '\n')
                for line in lines[int(len(lines) * percent):]:
                    id += 1
                    line.append(str(id))
                    dest_f.write(';'.join(line) + '\n')


@click.command()
@click.option('--duplicated_rows', help='Procent zduplikowanych wierszy')
@click.option('--swap_chance', help='Szansa na zamianę pół')
@click.option('--typo_percent', help='Procent zamienionych liter w nazwisku i imieniu')
def main(typo_percent, duplicated_rows, swap_chance):
    scramble(typo_percent, duplicated_rows, swap_chance)


if __name__ == "__main__":
    main()

