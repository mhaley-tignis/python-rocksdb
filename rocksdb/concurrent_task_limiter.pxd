from libcpp.string cimport string
from libc.stdint cimport int32_t

cdef extern from "concurrent_task_limiter_impl.h" namespace "rocksdb":
    cdef cppclass ConcurrentTaskLimiter:
        const string& GetName()
        void SetMaxOutstandingTask(int32_t)
        void ResetMaxOutstandingTask()
        int32_t GetOutstandingTask()

    ConcurrentTaskLimiter* NewConcurrentTaskLimiter(const string&, int32_t)
