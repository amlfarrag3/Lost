def get_possible_child_blood_types(mother_blood_type, father_blood_type):
    def split_type(bt):
        if bt[-1] in ['+', '-']:
            return bt[:-1], bt[-1]
        return bt, '+'

    m_type, m_rh = split_type(mother_blood_type)
    f_type, f_rh = split_type(father_blood_type)

    inheritance_map = {
        ('O', 'O'): ['O'],
        ('O', 'A'): ['A', 'O'],
        ('O', 'B'): ['B', 'O'],
        ('O', 'AB'): ['A', 'B'],
        ('A', 'A'): ['A', 'O'],
        ('A', 'B'): ['A', 'B', 'AB', 'O'],
        ('A', 'AB'): ['A', 'B', 'AB'],
        ('B', 'B'): ['B', 'O'],
        ('B', 'AB'): ['A', 'B', 'AB'],
        ('AB', 'AB'): ['A', 'B', 'AB'],
    }

    parents_pair = tuple(sorted((m_type, f_type)))
    possible_abo = inheritance_map.get(parents_pair, [])

    if m_rh == '-' and f_rh == '-':
        possible_rh = ['-']
    else:
        possible_rh = ['+', '-']

    return [abo + rh for abo in possible_abo for rh in possible_rh]

