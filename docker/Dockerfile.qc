FROM public.ecr.aws/lts/ubuntu:22.04

RUN apt-get update && apt-get install -y \
    fastp \
    && rm -rf /var/lib/apt/lists/*