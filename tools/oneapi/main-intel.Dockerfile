FROM intel/oneapi-basekit:latest

# Install necessary dependencies
RUN apt-get update && apt-get install -y cmake

# Copy the project files
COPY . /project
WORKDIR /project

# Build project
RUN if [ "${LLAMA_SYCL_F16}" = "ON" ]; then \
    echo "LLAMA_SYCL_F16 is set" && \
    export OPT_SYCL_F16="-DLLAMA_SYCL_F16=ON"; \
    else \
    export OPT_SYCL_F16=""; \
    fi && \
    cmake -B build -DLLAMA_SYCL=ON -DCMAKE_C_COMPILER=icx -DCMAKE_CXX_COMPILER=icpx ${OPT_SYCL_F16} && \
    cmake --build build --config Release --target main
