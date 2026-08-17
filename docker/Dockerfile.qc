FROM public.ecr.aws/lts/ubuntu:22.04

RUN apt-get update && apt-get install -y \
    fastp=0.20.1+dfsg-1 \
    && rm -rf /var/lib/apt/lists/*