#!/usr/bin/env python3

import sys
from fasta_iterator_class import FASTAReader

# simplified version without subdictionaries
def make_kmer_dict(k, seqs): 
    kmer_dict = {}
    for seq_id, sequence in seqs:
        # Use seq_id to make nested dictionary
        for i in range(0, len(sequence) - k + 1):
            kmer = sequence[i:(i+k)]
            if kmer not in kmer_dict:
                kmer_dict[kmer] = []
            kmer_dict.setdefault(kmer, [])
            if kmer in kmer_dict:
                kmer_dict[kmer].append(i) 
    return kmer_dict

# real version with subdictionaries
def make_kmer_dict2(k, seqs): 
    kmer_dict = {}
    for seq_id, sequence in seqs:
        seq_id_dict = {}
        for i in range(0, len(sequence) - k + 1):
            kmer = sequence[i:(i+k)]
            if kmer not in seq_id_dict:
                seq_id_dict[kmer] = []
            seq_id_dict.setdefault(kmer, [])
            if kmer in seq_id_dict:
                seq_id_dict[kmer].append(i)       
        kmer_dict[seq_id] = seq_id_dict
    return kmer_dict

# loop through target dictionaries
target_seqs = FASTAReader(open('subset.fa'))
target_kmers = {}
target_dicts = make_kmer_dict2(11, target_seqs)

# loop through query – you can use the first version because there is only one sequnce 
# in the FASTA file
query_seqs = FASTAReader(open('droYak2_seq.fa'))
query_kmers = {}
query_dict = make_kmer_dict(11, query_seqs)

for query_key in query_dict.keys():
    for target_dict in target_dicts.keys(): 
        if query_key in target_dicts[target_dict].keys():
            print(target_dict, target_dicts[target_dict][query_key], query_dict[query_key], query_key, sep = '\t')
