FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies and clean up in one layer to reduce image size
RUN apt-get update && apt-get install -y \
    wget \
    bwa \
    samtools \
    unzip \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install AWS CLI v2
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "/tmp/awscliv2.zip" \
    && unzip /tmp/awscliv2.zip -d /tmp \
    && /tmp/aws/install \
    && rm -rf /tmp/aws /tmp/awscliv2.zip


# Copy the data download and alignment scripts
COPY download_and_upload.sh /usr/local/bin/download_and_upload.sh
COPY run_alignment.sh /usr/local/bin/run_alignment.sh
RUN chmod +x /usr/local/bin/download_and_upload.sh /usr/local/bin/run_alignment.sh

# Set a non-root user for security best practices
RUN useradd -m -u 1000 appuser
USER root
WORKDIR /home/appuser

# Default command (can be overridden by Batch job)
CMD ["/usr/local/bin/run_alignment.sh"]
