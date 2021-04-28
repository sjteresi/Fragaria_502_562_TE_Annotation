#!/usr/bin/env python3

"""
Reformat Fasta files for EDTA usage
"""

__author__ = "Scott Teresi"

import argparse
import os
import logging
import coloredlogs

import Bio
from Bio import SeqIO

import re


def reformat_seq_iq(input_fasta, genome_name, output_dir, logger):
    new_fasta = os.path.join(output_dir, (genome_name + "_CDS_NewNames.fasta"))
    name_key = os.path.join(output_dir, (genome_name + "_CDS_Seq_ID_Conversion.txt"))

    if os.path.exists(new_fasta):
        os.remove(new_fasta)  # remove the file because we are in append mode
    if os.path.exists(name_key):
        os.remove(name_key)
    name_num = 1
    pair_dict = {}  # NB this is used to write the conversion key later for
    # clarity
    with open(input_fasta, "r") as input_fasta:
        for s_record in SeqIO.parse(input_fasta, "fasta"):
            # NB the s_record.id and s_record.description combined contain
            # all the information for each entry following the '>' character
            # in the fasta
            s_record.id = s_record.id.split("_")[-1]
            pair_dict[s_record.id] = s_record.description
            s_record.description = ""  # NB edit the description so that when
            # we rewrite we don't have the extraneous info
            with open(new_fasta, "a") as output:
                SeqIO.write(s_record, output, "fasta")
    logger.info(
        "Finished writing new fasta to: %s" % os.path.join(output_dir, new_fasta)
    )

    with open(name_key, "w") as output:
        for key, val in pair_dict.items():
            # Write the conversion table for record-keeping.
            output.write("%s\t%s\n" % (key, val))
    logger.info("Finished writing conversion table to: %s" % name_key)


if __name__ == "__main__":

    path_main = os.path.abspath(__file__)
    dir_main = os.path.dirname(path_main)
    parser = argparse.ArgumentParser(description="Reformat FASTA for EDTA")

    parser.add_argument("fasta_input_file", type=str, help="parent path of fasta file")
    parser.add_argument("genome_id", type=str, help="genome name")
    # NB path declared below
    output_default = os.path.join(dir_main, "../results")
    parser.add_argument(
        "--output_dir",
        "-o",
        type=str,
        default=output_default,
        help="Parent directory to output results",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="set debugging level to DEBUG"
    )
    args = parser.parse_args()
    args.fasta_input_file = os.path.abspath(args.fasta_input_file)
    args.output_dir = os.path.abspath(args.output_dir)

    log_level = logging.DEBUG if args.verbose else logging.INFO
    logger = logging.getLogger(__name__)
    coloredlogs.install(level=log_level)

    reformat_seq_iq(args.fasta_input_file, args.genome_id, args.output_dir, logger)
