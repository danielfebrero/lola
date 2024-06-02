ARG ONEAPI_VERSION=2024.0.1-devel-ubuntu22.04

FROM intel/oneapi-basekit:$ONEAPI_VERSION as build

# Adding Intel oneAPI repository keys and lists
RUN wget -O- https://apt.repos.intel.com/intel-gpg-keys/GPG-PUB-KEY-INTEL-SW-PRODUCTS.PUB | gpg --dearmor | tee /usr/share/keyrings/intel-oneapi-archive-keyring.gpg > /dev/null && \
    echo "deb [signed-by=/usr/share/keyrings/intel-oneapi-archive-keyring.gpg] https://apt.repos.intel.com/oneapi all main " | tee /etc/apt/sources.list.d/oneAPI.list && \
    chmod 644 /usr/share/keyrings/intel-oneapi-archive-keyring.gpg && \
    rm /etc/apt/sources.list.d/intel-graphics.list && \
    wget -O- https://repositories.intel.com/graphics/intel-graphics.key | gpg --dearmor | tee /usr/share/keyrings/intel-graphics.gpg > /dev/null && \
    echo "deb [arch=amd64,i386 signed-by=/usr/share/keyrings/intel-graphics.gpg] https://repositories.intel.com/graphics/ubuntu jammy arc" | tee /etc/apt/sources.list.d/intel.gpu.jammy.list && \
    chmod 644 /usr/share/keyrings/intel-graphics.gpg

# Set LLAMA_SYCL_F16 environment variable default
ARG LLAMA_SYCL_F16=OFF

# Install necessary packages
RUN apt-get update && \
    apt-get install -y git cmake

# Set working directory
WORKDIR /app

# Copy CMakeLists.txt
COPY ./CMakeLists.txt ./CMakeLists.txt

# Copy source files
COPY ./lola.cpp ./lola.cpp

RUN cp lola.cpp main.cpp

# Build project
RUN if [ "${LLAMA_SYCL_F16}" = "ON" ]; then \
    echo "LLAMA_SYCL_F16 is set" && \
    export OPT_SYCL_F16="-DLLAMA_SYCL_F16=ON"; \
    else \
    export OPT_SYCL_F16=""; \
    fi && \
    cmake -B build -DLLAMA_SYCL=ON -DCMAKE_C_COMPILER=icx -DCMAKE_CXX_COMPILER=icpx ${OPT_SYCL_F16} && \
    cmake --build build --config Release --target main

# Create runtime image
FROM intel/oneapi-basekit:$ONEAPI_VERSION as runtime

# Copy the built binary from the build stage
COPY --from=build /app/build/bin/main /main

# Set locale
ENV LC_ALL=C.utf8

# Entry point
ENTRYPOINT [ "/main" ]
