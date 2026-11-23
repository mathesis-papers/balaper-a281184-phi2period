import argparse
from hashlib import sha256
import json
from math import comb
from pathlib import Path


def multiply(left, right, modulus=None, dimension=None):
    result = [0] * (len(left) + len(right) - 1)
    for left_index, left_value in enumerate(left):
        for right_index, right_value in enumerate(right):
            index = left_index + right_index
            if dimension is None or index < dimension:
                result[index] += left_value * right_value
    if dimension is not None:
        result = (result + [0] * dimension)[:dimension]
    if modulus:
        result = [value % modulus for value in result]
    return result


def derivative(polynomial):
    return [index * value for index, value in enumerate(polynomial)][1:] or [0]


def add(left, right):
    length = max(len(left), len(right))
    return [(left[index] if index < len(left) else 0)
            + (right[index] if index < len(right) else 0) for index in range(length)]


def operator(polynomial, modulus=None, dimension=None, parity=1, flow_exponent=4):
    first = derivative(polynomial)
    auxiliary = add([parity * value for value in polynomial],
                    [2 * value for value in multiply([1, 1], first)])
    inside = add(multiply([1, parity + flow_exponent - 1], auxiliary),
                 [2 * value for value in multiply([0, 1, 1], derivative(auxiliary))])
    outer = [comb(flow_exponent - 2, index) for index in range(flow_exponent - 1)]
    return multiply(outer, inside, modulus, dimension)


def polynomial_values(count, modulus=None, dimension=None, exponent=3, flow_exponent=4):
    parity = exponent % 2
    power = (exponent - parity) // 2
    polynomial = [comb(power, index) for index in range(power + 1)]
    values = []
    for index in range(count + 1):
        values.append(polynomial[0])
        if index < count:
            polynomial = operator(polynomial, modulus, dimension, parity, flow_exponent)
    return values


def recurrence_values(count, exponent=3, flow_exponent=4):
    step = 2 * flow_exponent - 2
    previous = [1] * (exponent + step * count + 1)
    values = [previous[exponent]]
    for index in range(1, count + 1):
        bound = exponent + step * (count - index)
        current = [power * (power + flow_exponent - 1) * previous[power + step]
                   - power * (power + flow_exponent - 2) * previous[power + step - 2]
                   for power in range(bound + 1)]
        values.append(current[exponent])
        previous = current
    return values


def totient(number):
    result = number
    factor = 2
    remaining = number
    while factor * factor <= remaining:
        if remaining % factor == 0:
            result -= result // factor
            while remaining % factor == 0:
                remaining //= factor
        factor += 1
    if remaining > 1:
        result -= result // remaining
    return result


def exponent_bound(number):
    bound = 1
    factor = 2
    remaining = number
    while factor <= remaining:
        exponent = 0
        while remaining % factor == 0:
            remaining //= factor
            exponent += 1
        bound = max(bound, exponent)
        factor += 1
    return bound


def prime_divisors(number):
    divisors = []
    factor = 2
    while factor <= number:
        if number % factor == 0:
            divisors.append(factor)
            while number % factor == 0:
                number //= factor
        factor += 1
    return divisors


def source_certificate(oeis, flow, exponent, modulus, period, first_index,
                       offset=0, row_shift=None, row_multiplier=None):
    dimension = (modulus + 1) // 2
    start = first_index - offset
    values = polynomial_values(start + 2 * period + dimension, modulus, dimension,
                               exponent, flow)
    differences = [(values[index + period] - values[index]) % modulus
                   for index in range(start, start + dimension)]
    assert differences == [0] * dimension
    witnesses = []
    for prime in prime_divisors(period):
        smaller = period // prime
        index = next(index for index in range(start, start + period)
                     if values[index + smaller] != values[index])
        witnesses.append({'prime': prime, 'excluded_shift': smaller,
                          'index': index + offset, 'value': values[index],
                          'shifted_value': values[index + smaller]})
    result = {'oeis': oeis, 'flow_exponent': flow, 'observable_exponent': exponent,
              'modulus': modulus, 'least_period': period, 'first_index': first_index,
              'coefficient_index_offset': offset, 'dimension': dimension,
              'period_zero_differences': differences, 'minimality_witnesses': witnesses,
              'first_period': values[start:start + period]}
    if start > 0:
        assert values[start - 1] != values[start - 1 + period]
        result['onset_witness'] = {'index': first_index - 1,
                                   'value': values[start - 1],
                                   'shifted_value': values[start - 1 + period]}
    if row_shift is not None:
        row_differences = [(values[index + row_shift] - row_multiplier * values[index]) % modulus
                           for index in range(start, start + dimension)]
        assert row_differences == [0] * dimension
        result['row_relation'] = {'shift': row_shift, 'multiplier': row_multiplier,
                                  'zero_differences': row_differences}
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    parser.add_argument('--bfile', type=Path)
    args = parser.parse_args()
    count = 256
    recurrence = recurrence_values(count)
    independent = polynomial_values(count)
    assert recurrence == independent
    family_comparisons = []
    for flow, exponent in [(4, 0), (4, 1), (4, 2), (4, 4), (5, 1), (6, 1), (8, 1), (8, 8)]:
        assert recurrence_values(64, exponent, flow) == polynomial_values(64, exponent=exponent,
                                                                         flow_exponent=flow)
        family_comparisons.append({'flow_exponent': flow, 'observable_exponent': exponent,
                                    'comparisons': 65})
    if args.bfile:
        source = {}
        for line in args.bfile.read_text().splitlines():
            if line.strip() and not line.lstrip().startswith('#'):
                index, value = map(int, line.split())
                source[index] = value
        assert set(source) == set(range(101))
        assert all(recurrence[index] == value for index, value in source.items())
    dimension = 6
    columns = [operator([0] * index + [1], 11, dimension)
               for index in range(dimension)]
    matrix = [[columns[column][row] for column in range(dimension)]
              for row in range(dimension)]
    values = polynomial_values(40, 11, dimension)
    certificate = [((values[index + 5] - 5 * values[index]) % 11)
                   for index in range(1, 7)]
    assert certificate == [0] * dimension
    assert values[1] == 3 and values[6] == 4
    assert values[0] == 1 and values[25] == 3
    assert pow(5, 5, 11) == 1
    assert [pow(5, index, 11) for index in range(1, 5)] == [5, 3, 4, 9]
    modular = []
    for modulus in [2, 3, 4, 8, 9, 11, 12, 16, 25, 27, 32, 49, 72, 100]:
        start = exponent_bound(modulus)
        shift = totient(modulus) ** 2
        residues = polynomial_values(start + shift + 63, modulus, (modulus + 1) // 2)
        assert all(residues[index + shift] == residues[index]
                   for index in range(start, start + 64))
        modular.append({'modulus': modulus, 'first_index': start,
                        'shift': shift, 'comparisons': 64})
    companion_certificates = []
    for modulus, shift, start in [(10, 8, 0), (9, 3, 1), (12, 1, 0)]:
        rank = (modulus + 1) // 2
        residues = polynomial_values(start + shift + rank - 1, modulus, rank, exponent=1)
        differences = [(residues[index + shift] - residues[index]) % modulus
                       for index in range(start, start + rank)]
        assert differences == [0] * rank
        companion_certificates.append({'oeis': 'A281181', 'modulus': modulus,
                                       'shift': shift, 'first_index': start,
                                       'dimension': rank, 'zero_differences': differences,
                                       'initial_values': residues[:start + shift]})
    source_periods = [
        source_certificate('A281180', 4, 4, 7, 18, 1, offset=1,
                           row_shift=6, row_multiplier=2),
        source_certificate('A281181', 4, 1, 10, 8, 0),
        source_certificate('A281181', 4, 1, 9, 3, 1),
        source_certificate('A281181', 4, 1, 13, 72, 0,
                           row_shift=6, row_multiplier=7),
        source_certificate('A281183', 4, 2, 11, 25, 1,
                           row_shift=5, row_multiplier=5),
        source_certificate('A281184', 4, 3, 11, 25, 1,
                           row_shift=5, row_multiplier=5),
        source_certificate('A281440', 8, 1, 13, 72, 0,
                           row_shift=6, row_multiplier=6),
        source_certificate('A281428', 5, 1, 27, 18, 2),
    ]
    vanishing_certificates = []
    for prime, start in [(5, 3), (7, 4), (11, 6)]:
        rank = (prime + 1) // 2
        residues = polynomial_values(start + rank - 1, prime, rank,
                                     exponent=1, flow_exponent=5)
        assert residues[start:] == [0] * rank
        assert residues[start - 1] != 0
        vanishing_certificates.append({'oeis': 'A281428', 'modulus': prime,
                                       'dimension': rank, 'first_zero_index': start,
                                       'zero_values': residues[start:],
                                       'preceding_value': residues[start - 1]})
    odd_values_mod385 = polynomial_values(6, 385, 193, exponent=1, flow_exponent=5)
    assert odd_values_mod385 == [1, 1, 17, 95, 315, 105, 0]
    assert polynomial_values(7, 13, 7, exponent=1, flow_exponent=8) == [1, 1, 3, 5, 7, 8, 6, 6]
    full_index_parity = []
    even_values = polynomial_values(6, 2, 1, exponent=1)
    odd_values = polynomial_values(6, 2, 1, exponent=4)
    for index in range(12):
        full_index_parity.append((even_values if index % 2 == 0 else odd_values)[index // 2])
    assert full_index_parity == [1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
    output = {
        'schema_version': 1,
        'coefficient_methods': ['integer fixed-column recurrence',
                                'integer polynomial differential operator in S squared'],
        'coefficient_comparisons': count + 1,
        'family_coefficient_comparisons': family_comparisons,
        'initial_values': recurrence[:10],
        'value_256': str(recurrence[256]),
        'value_256_decimal_sha256': sha256(str(recurrence[256]).encode()).hexdigest(),
        'mod11_matrix_rows': matrix,
        'mod11_dimension': dimension,
        'mod11_five_step_difference_certificate_n1_to_n6': certificate,
        'mod11_tail_n1_to_n25': values[1:26],
        'mod11_minimality_witness': {'index': 1, 'shift': 5,
                                    'value': values[1], 'shifted_value': values[6]},
        'mod11_preperiod_witness': {'index': 0, 'shift': 25,
                                   'value': values[0], 'shifted_value': values[25]},
        'finite_modular_controls': modular,
        'companion_period_certificates': companion_certificates,
        'source_least_period_certificates': source_periods,
        'A281428_prime_vanishing_certificates': vanishing_certificates,
        'A281428_mod385_initial_values': odd_values_mod385,
        'A281182_mod2_initial_values': full_index_parity,
        'infinite_period_certificate':
            'Six initial zero scalar differences and Cayley-Hamilton give '
            'a(n+5)=5*a(n) modulo 11 for every n>=1; hence the least tail period is 25.',
        'general_modulus_theorem':
            'Su (2026), Theorem 3.2 and Corollary 3.3; the additional modular controls are finite checks.'
    }
    if args.bfile:
        output['bfile_comparisons'] = 101
    text = json.dumps(output, indent=2) + '\n'
    if args.output:
        args.output.write_text(text)
    else:
        print(text, end='')


if __name__ == '__main__':
    main()
