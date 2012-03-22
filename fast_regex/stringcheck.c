//http://stackoverflow.com/questions/1323364/in-python-how-to-check-if-a-string-only-contains-certain-characters
#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <string.h>
// length 69
char ss[][69] = {"myself", "ours", "ourselves", "your", "yours", "yourself", "yourselves",  "himself", "hers", "herself",  "itself", "they", "them", "their", "theirs", "themselves", "what", "which",  "whom", "this", "that", "these", "those",  "were",  "been", "being", "have",  "having",  "does", "doing",  "because",  "until", "while",  "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below",  "from",  "down", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where",  "both", "more", "most", "other", "some", "such",  "only",  "same",  "than",  "very",  "will", "just",  "should" };

static PyObject *check(PyObject *self, PyObject *args)
{


        const char *s;
        Py_ssize_t count, ii, i;
        char c;
        const char *cc;
        if (0 == PyArg_ParseTuple (args, "s#", &s, &count)) {
                return NULL;
        }

		if (count <= 3) { Py_RETURN_FALSE; } 

        for (ii = 0; ii < count; ii++) {
                c = s[ii];
                if ((c < '0') || c > 'z') {
                        Py_RETURN_FALSE;
                }
                if (c > '9' && c < 'a') {
                        Py_RETURN_FALSE;
                }
        }

		for(i = 0; i < 69; i++)
		{
          cc = ss[i];
		  if (strcmp(cc,s) == 0) {  Py_RETURN_FALSE;  } 
		}		

        Py_RETURN_TRUE;
}

PyDoc_STRVAR (DOC, "Fast stringcheck");
static PyMethodDef PROCEDURES[] = {
        {"check", (PyCFunction) (check), METH_VARARGS, NULL},
        {NULL, NULL}
};
PyMODINIT_FUNC
initstringcheck (void) {
        Py_InitModule3 ("stringcheck", PROCEDURES, DOC);
}

/*static PyObject *check(PyObject *self, PyObject *args)
{
        const char *s;
        Py_ssize_t count, ii;
        char c;
        if (0 == PyArg_ParseTuple (args, "s#", &s, &count)) {
                return NULL;
        }

		if (count <= 3) { Py_RETURN_FALSE; } 

        for (ii = 0; ii < count; ii++) {
                c = s[ii];
                if ((c < '0') || c > 'z') {
                        Py_RETURN_FALSE;
                }
                if (c > '9' && c < 'a') {
                        Py_RETURN_FALSE;
                }
        }

        Py_RETURN_TRUE;
}

PyDoc_STRVAR (DOC, "Fast stringcheck");
static PyMethodDef PROCEDURES[] = {
        {"check", (PyCFunction) (check), METH_VARARGS, NULL},
        {NULL, NULL}
};
PyMODINIT_FUNC
initstringcheck (void) {
        Py_InitModule3 ("stringcheck", PROCEDURES, DOC);
}*/
