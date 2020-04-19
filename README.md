# Partition Table Parser
Python implementation for a Master Boot Record and GUID Partition Table parser

# Usage

partition_tables |image_name| |image_type| |sector_size|

image_name: a .dd file

image_type: use either "mbr" or "gpt"

sector_size: if parsing "mbr" set this value to 512
