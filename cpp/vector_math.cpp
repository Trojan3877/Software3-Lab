// cpp/vector_math.cpp
// --------------------------------------------------------------
// Build (Linux / macOS):
//   g++ -O3 -shared -std=c++17 -fPIC vector_math.cpp -o libvector.so
//
// Windows (MSVC):
//   cl /O2 /LD vector_math.cpp /Fe:vector.dll
//
// Exposed functions
//   • double dot(const double* a, const double* b, std::size_t n)
//   • double cosine_similarity(const double* a, const double* b, std::size_t n)
// --------------------------------------------------------------

#include <cmath>
#include <cstddef>

extern "C" {

/* ──────────────────────────────────────────────────────────────
   Compute dot product of two vectors.
   a, b : pointers to double arrays
   n    : length of vectors
   Returns Σ aᵢ · bᵢ
──────────────────────────────────────────────────────────────── */
double dot(const double* a, const double* b, std::size_t n)
{
    double result = 0.0;
    for (std::size_t i = 0; i < n; ++i)
        result += a[i] * b[i];
    return result;
}

/* ──────────────────────────────────────────────────────────────
   Compute cosine similarity ∈ [-1, 1].
   Returns 0.0 if either vector has zero magnitude.
──────────────────────────────────────────────────────────────── */
double cosine_similarity(const double* a, const double* b, std::size_t n)
{
    double mag_a = 0.0, mag_b = 0.0, dot_ab = 0.0;

    for (std::size_t i = 0; i < n; ++i) {
        dot_ab += a[i] * b[i];
        mag_a  += a[i] * a[i];
        mag_b  += b[i] * b[i];
    }

    const double denom = std::sqrt(mag_a) * std::sqrt(mag_b);
    return (denom == 0.0) ? 0.0 : dot_ab / denom;
}

} // extern "C"
