#!/usr/bin/env python3
"""
Sandhi Splitter Module
----------------------
A rule-based engine to split Telugu words based on grammatical Sandhi rules.

Compliance:
- Contains only function definitions (no global execution).
- Uses standard Python typing and docstrings.

Author: Swecha Contributor
Date: 2025-10-25
"""

# Telugu Character Definitions
TELUGU_CONSONANTS = "కఖగఘఙచఛజఝఞటఠడఢణతథదధనపఫబభమయరలవశషసహళక్షఱ"
VIRAMA = '్'
VOWELS = "అఆఇఈఉఊఋౠఎఏఐఒఓఔ"
MATRA_MAP = {
    'ా': 'ఆ', 'ి': 'ఇ', 'ీ': 'ఈ', 'ు': 'ఉ', 'ూ': 'ఊ', 'ృ': 'ఋ', 'ౄ': 'ౠ',
    'ె': 'ఎ', 'ే': 'ఏ', 'ై': 'ఐ', 'ొ': 'ఒ', 'ో': 'ఓ', 'ౌ': 'ఔ'
}
VOWEL_TO_MATRA = {v: k for k, v in MATRA_MAP.items()}

def find_consonant_cluster_start(word, end_index):
    """Helper to find the start of a consonant cluster before a given index."""
    start_index = -1
    j = end_index - 1
    while j >= 0:
        current_char = word[j]
        if current_char in TELUGU_CONSONANTS:
            if j == 0 or word[j-1] != VIRAMA:
                start_index = j
                break
        elif current_char != VIRAMA:
            break
        j -= 1
    return start_index

# --- Sandhi Rules ---

def split_savarnadeergha(word):
    """Splits word based on Savarnadeergha Sandhi."""
    sandhi_map = {'ా': ('అ', ''), 'ీ': ('ఇ', 'ి'), 'ూ': ('ఉ', 'ు'), 'ౄ': ('ఋ', 'ృ')}
    splits = []
    for i, char in enumerate(word):
        if char in sandhi_map:
            start_of_cluster = find_consonant_cluster_start(word, i)
            if start_of_cluster != -1:
                short_vowel_char, short_matra = sandhi_map[char]
                prefix = word[:start_of_cluster]
                consonant = word[start_of_cluster:i]
                word1 = prefix + consonant + short_matra if short_matra else prefix + consonant
                word2 = short_vowel_char + word[i+1:]
                splits.append(f"'{word1}' + '{word2}'")
    return splits

def split_utva_ikara_sandhi(word):
    """Splits word based on Utva/Ikara Sandhi."""
    splits = []
    possible_elided_matras = {'ు': 'ఉ', 'ి': 'ఇ'}
    for i in range(1, len(word)):
        current_char = word[i]
        if current_char in MATRA_MAP:
            start_of_cluster = find_consonant_cluster_start(word, i)
            if start_of_cluster != -1:
                prefix = word[:start_of_cluster]
                consonant = word[start_of_cluster:i]
                word2_start_vowel = MATRA_MAP[current_char]
                word2 = word2_start_vowel + word[i+1:]
                for matra, vowel in possible_elided_matras.items():
                    word1 = prefix + consonant + matra
                    splits.append(f"'{word1}' + '{word2}'")
    return splits

def split_yadagama_sandhi(word):
    """Splits word based on Yadagama Sandhi."""
    splits = []
    for i in range(1, len(word) - 1):
        if word[i] == 'య' and i > 1 and word[i-1] == 'ి' and word[i-2] in TELUGU_CONSONANTS:
            if (i + 1 < len(word)) and (word[i+1] not in MATRA_MAP and word[i+1] in TELUGU_CONSONANTS):
                 word1 = word[:i]
                 word2 = "అ" + word[i+1:]
                 splits.append(f"'{word1}' + '{word2}'")
            elif (i + 1 < len(word)) and word[i+1] in MATRA_MAP:
                 word1 = word[:i]
                 word2 = MATRA_MAP[word[i+1]] + word[i+2:]
                 splits.append(f"'{word1}' + '{word2}'")
    return splits

def split_amredita_sandhi(word):
    """Splits word based on Amredita Sandhi."""
    splits = []
    mid = len(word) // 2
    if len(word) > 1 and len(word) % 2 == 0 and word[:mid] == word[mid:]:
        splits.append(f"'{word[:mid]}' + '{word[mid:]}'")
    return splits

def split_gasada_dava_adesa(word):
    """Splits word based on Gasadadava Adesa Sandhi."""
    splits = []
    reverse_map = {'గ': 'క', 'స': 'చ', 'డ': 'ట', 'ద': 'త', 'వ': 'ప'}
    for i, char in enumerate(word):
        if char in reverse_map:
            start_of_cluster = find_consonant_cluster_start(word, i)
            if start_of_cluster != -1:
                word1_candidate = word[:start_of_cluster]
                if len(word1_candidate) > 1:
                    word1 = word1_candidate
                    original_consonant = reverse_map[char]
                    suffix = word[start_of_cluster:]
                    word2 = original_consonant + suffix[1:]
                    splits.append(f"'{word1}' + '{word2}'")
    return splits

def split_trika(word):
    """Splits word based on Trika Sandhi."""
    splits = []
    trika_vowels = {'అ': 'ఆ', 'ఇ': 'ఈ', 'ఎ': 'ఏ'}
    if len(word) > 3 and word[0] in trika_vowels:
        if word[2] == '్' and word[1] == word[3]:
            word1 = trika_vowels[word[0]]
            word2 = word[3:]
            splits.append(f"'{word1}' + '{word2}'")
    return splits

def split_guna(word):
    """Splits word based on Guna Sandhi."""
    sandhi_map = {'ే': ('ఇ', 'ఈ'), 'ో': ('ఉ', 'ఊ')}
    splits = []
    for i, char in enumerate(word):
        if char in sandhi_map:
            start_of_cluster = find_consonant_cluster_start(word, i)
            if start_of_cluster != -1:
                prefix = word[:start_of_cluster]
                consonant = word[start_of_cluster:i]
                word1_a = prefix + consonant
                vowel1, vowel2 = sandhi_map[char]
                suffix = word[i+1:]
                splits.append(f"'{word1_a}' + '{vowel1 + suffix}'")
                splits.append(f"'{word1_a}' + '{vowel2 + suffix}'")
    return splits

def split_vriddhi(word):
    """Splits word based on Vriddhi Sandhi."""
    sandhi_map = {'ై': ('ఏ', 'ఐ'), 'ౌ': ('ఓ', 'ఔ')}
    splits = []
    for i, char in enumerate(word):
        if char in sandhi_map:
            start_of_cluster = find_consonant_cluster_start(word, i)
            if start_of_cluster != -1:
                prefix = word[:start_of_cluster]
                consonant = word[start_of_cluster:i]
                word1_a = prefix + consonant
                vowel1, vowel2 = sandhi_map[char]
                suffix = word[i+1:]
                splits.append(f"'{word1_a}' + '{vowel1 + suffix}'")
                splits.append(f"'{word1_a}' + '{vowel2 + suffix}'")
    return splits

def split_yanadesa(word):
    """Splits word based on Yanadesa Sandhi."""
    splits = []
    for i in range(1, len(word)):
        if word[i] == '్' and i + 1 < len(word):
            base_consonant_char = word[i-1]
            adesa_char = word[i+1]

            original_matra = None
            if adesa_char == 'య': original_matra = 'ి'
            elif adesa_char == 'వ': original_matra = 'ు'
            elif adesa_char == 'ర': original_matra = 'ృ'

            if original_matra:
                cluster_and_matra = word[i+2:]
                next_char = cluster_and_matra[0] if cluster_and_matra else ''
                vowel_sound = MATRA_MAP.get(next_char, 'అ')

                word1 = word[:i-1] + base_consonant_char + original_matra
                word2 = vowel_sound + (cluster_and_matra[1:] if next_char in MATRA_MAP else cluster_and_matra)
                splits.append(f"'{word1}' + '{word2}'")
    return splits

def split_jashtva(word):
    """Splits word based on Jashtva Sandhi."""
    splits = []
    reverse_map = {'గ': 'క', 'జ': 'చ', 'డ': 'ట', 'ద': 'త', 'బ': 'ప'}
    for i, char in enumerate(word):
        if char in reverse_map:
            vowel_of_char = 'అ'
            suffix_start_index = i + 1
            if i + 1 < len(word) and word[i+1] in MATRA_MAP:
                vowel_of_char = MATRA_MAP[word[i+1]]
                suffix_start_index = i + 2

            word1 = word[:i] + reverse_map[char] + VIRAMA
            word2 = vowel_of_char + word[suffix_start_index:]
            splits.append(f"'{word1}' + '{word2}'")
    return splits

def split_schutva(word):
    """Splits word based on Schutva Sandhi."""
    splits = []
    if 'చ్చ' in word:
        index = word.find('చ్చ')
        word1 = word[:index] + 'త్'
        word2 = 'చ' + word[index+2:]
        splits.append(f"'{word1}' + '{word2}'")
    if 'శ్శ' in word:
        index = word.find('శ్శ')
        word1 = word[:index] + 'స్'
        word2 = 'శ' + word[index+2:]
        splits.append(f"'{word1}' + '{word2}'")
    return splits

def split_anunasika(word):
    """Splits word based on Anunasika Sandhi."""
    splits = []
    reverse_map = {'ఙ': 'క', 'ఞ': 'చ', 'ణ': 'ట', 'న': 'త', 'మ': 'ప'}
    for i in range(1, len(word)):
        if word[i] == '్' and word[i-1] in reverse_map:
            nasal = word[i-1]
            word1 = word[:i-1] + reverse_map[nasal] + VIRAMA
            word2 = word[i+1:]
            splits.append(f"'{word1}' + '{word2}'")
    if 'న్న' in word:
        index = word.find('న్న')
        word1 = word[:index] + 'త్'
        word2 = 'న' + word[index+2:]
        splits.append(f"'{word1}' + '{word2}'")
    return splits

def find_all_splits(word):
    """Executes all defined Sandhi functions on the input word."""
    all_splits = {
        "savarnadeergha": split_savarnadeergha(word),
        "guna": split_guna(word),
        "vriddhi": split_vriddhi(word),
        "yanadesa": split_yanadesa(word),
        "utva_ikara": split_utva_ikara_sandhi(word),
        "yadagama": split_yadagama_sandhi(word),
        "gasada_dava": split_gasada_dava_adesa(word),
        "amredita": split_amredita_sandhi(word),
        "trika": split_trika(word),
        "jashtva": split_jashtva(word),
        "schutva": split_schutva(word),
        "anunasika": split_anunasika(word),
    }
    return {k: list(set(v)) for k, v in all_splits.items() if v}