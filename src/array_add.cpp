#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <vector>

namespace py = pybind11;

py::array_t<double> add_arrays(py::array_t<double> input1, py::array_t<double> input2) {
    py::buffer_info buf1 = input1.request();
    py::buffer_info buf2 = input2.request();

    if (buf1.size != buf2.size) {
        throw std::runtime_error("Input arrays must have the same size");
    }

    double* ptr1 = static_cast<double*>(buf1.ptr);
    double* ptr2 = static_cast<double*>(buf2.ptr);

    std::vector<double> result(buf1.size);
    for (size_t i = 0; i < buf1.size; i++) {
        result[i] = ptr1[i] + ptr2[i];
    }

    return py::array_t<double>(buf1.size, result.data());
}

PYBIND11_MODULE(array_add, m) {
    m.doc() = "pybind11 example for adding NumPy arrays in C++";
    m.def("add_arrays", &add_arrays, "Add two NumPy arrays element-wise");
}
