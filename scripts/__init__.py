INSTRUMENT_MODEL_MAPPING = {
    "HISEQ_X_10": 9,
    "Illumina Genome Analyzer II": 11,
    "HISEQ_2000": 16,
    "HISEQ_2500": 17,
    "HISEQ_4000": 19,
    "ISEQ_100": 21,
    "MISEQ": 22,
    "NOVA_SEQ_X": 24,
    "NOVA_SEQ_6000": 25,
    "NEXT_SEQ_500": 26,
    "NEXT_SEQ_2000": 29,
    "unspecified": 30
}

LIBRARY_LAYOUT = ["SINGLE", "PAIRED"]

LIBRARY_STRATEGY = [
    "WGS",
    "WGA",
    "WXS",
    "RNA-Seq",
    "ssRNA-seq",
    "miRNA-Seq",
    "ncRNA-Seq",
    "FL-cDNA",
    "EST",
    "Hi-C",
    "ATAC-seq",
    "WCS",
    "RAD-Seq",
    "CLONE",
    "POOLCLONE",
    "AMPLICON",
    "CLONEEND",
    "FINISHING",
    "ChIP-Seq",
    "MNase-Seq",
    "DNase-Hypersensitivity",
    "Bisulfite-Seq",
    "CTS",
    "MRE-Seq",
    "MeDIP-Seq",
    "MBD-Seq",
    "Tn-Seq",
    "VALIDATION",
    "FAIRE-seq",
    "SELEX",
    "RIP-Seq",
    "ChIA-PET",
    "Synthetic-Long-Read",
    "Targeted-Capture",
    "Tethered Chromatin Conformation Capture",
    "NOMe-Seq",
    "ChM-Seq",
    "GBS",
    "OTHER",
    "snRNA-seq",
    "Ribo-Seq"
]

LIBRARY_SOURCE = [
    "GENOMIC",
    "GENOMIC SINGLE CELL",
    "TRANSCRIPTOMIC",
    "TRANSCRIPTOMIC SINGLE CELL",
    "METAGENOMIC",
    "METATRANSCRIPTOMIC",
    "SYNTHETIC",
    "VIRAL RNA",
    "OTHER"
]

LIBRARY_SELECTION = [
    "RANDOM",
    "PCR",
    "RANDOM PCR",
    "RT-PCR",
    "HMPR",
    "MF",
    "repeat fractionation",
    "size fractionation",
    "MSLL",
    "cDNA",
    "cDNA_randomPriming",
    "cDNA_oligo_dT",
    "PolyA",
    "Oligo-dT",
    "Inverse rRNA",
    "Inverse rRNA selection",
    "ChIP",
    "ChIP-Seq",
    "MNase",
    "DNase",
    "Hybrid Selection",
    "Reduced Representation",
    "Restriction Digest",
    "5-methylcytidine antibody",
    "MBD2 protein methyl-CpG binding domain",
    "CAGE",
    "RACE",
    "MDA",
    "padlock probes capture method",
    "other",
    "unspecified",
]

RUN_FILE_TYPE = [
    "srf",
    "sff"
    "fastq",
    "Illumina_native",
    "Illumina_native_qseq",
    "SOLiD_native_csfasta",
    "PacBio_HDF5",
    "bam",
    "cram",
    "CompleteGenomics_native",
    "OxfordNanopore_native",
]
