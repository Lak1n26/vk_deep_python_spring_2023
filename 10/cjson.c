
#include <stdio.h>
#include <string.h>
#include <string.h>
#include <stdbool.h>

#include <Python.h>



PyObject* cjson_loads(PyObject* self, PyObject* args)
{
    PyObject* json_str;
    if (!PyArg_ParseTuple(args, "O", &json_str)) {
        return NULL;
    }

    Py_ssize_t json_len = PyUnicode_GET_LENGTH(json_str);

    PyObject *dict = PyDict_New();

    PyObject *key;
    PyObject *value;
    PyObject *new_word = PyUnicode_FromString("");

    bool value_is_int = false;
    bool is_str = false;
    PyObject *format_str;

    for(int i = 0; i < json_len; ++i) {
        char* character = PyUnicode_READ_CHAR((PyUnicodeObject *) json_str, i);

        if (character == ':') {
            key = new_word;
            new_word = PyUnicode_FromString("");

            if (PyUnicode_READ_CHAR((PyUnicodeObject *) json_str, i + 1) == '"' ||
                    (PyUnicode_READ_CHAR((PyUnicodeObject *) json_str, i + 1) == ' ' && PyUnicode_READ_CHAR((PyUnicodeObject *) json_str, i + 2) == '"'))
            {
                value_is_int = false;
            } else {
                value_is_int = true;
            }

        }

        else if ((character == ',' && is_str == false) || character == '}') {
            value = new_word;
            new_word = PyUnicode_FromString("");

            if (value_is_int) {
                PyDict_SetItem(dict, key, PyLong_FromString(PyUnicode_AsUTF8(value), NULL, 10));
                value_is_int = false;
            } else {
                PyDict_SetItem(dict, key, value);
            }
        }
        else if (character == ' ') {
            Py_ssize_t word_len = PyUnicode_GET_LENGTH(new_word);
            if (word_len > 0) {
                format_str = PyUnicode_FromFormat("%c", character);
                new_word = PyUnicode_Concat(new_word, format_str);
            }

        }

        else if (
                character != '"' &&
                character != '{'
            ) {
            format_str = PyUnicode_FromFormat("%c", character);
            new_word = PyUnicode_Concat(new_word, format_str);
        }
        else if (character == '"') {
            if (!is_str) {
                is_str = true;
            } else {
                is_str = false;
            }
        }
    }

    return dict;
}











PyObject* cjson_dumps(PyObject* self, PyObject* args)
{
    PyObject* my_dict;

    if (!PyArg_ParseTuple(args, "O", &my_dict)) {
        return NULL;
    }
    PyObject* key_obj;
    PyObject* value_obj;
    Py_ssize_t pos = 0;

    PyObject *result = PyUnicode_FromString("{");

    PyObject *key_str_p = Py_None;
    PyObject *value_str_p = Py_None;
    bool key_is_int = false;
    bool value_is_int = false;

    while (PyDict_Next(my_dict, &pos, &key_obj, &value_obj)) {

        key_str_p = Py_None;
        value_str_p = Py_None;

        key_is_int = false;
        value_is_int = false;


        if (PyLong_Check(key_obj)) {

            key_str_p = PyObject_Str(key_obj);


        } else {

            key_str_p = PyObject_Str(key_obj);

        }

        if (PyLong_Check(value_obj)) {
            value_str_p = PyLong_AsLong(value_obj);
            value_is_int = true;
        } else {
            value_str_p = PyObject_Str(value_obj);
        }

        if (value_str_p != Py_None && key_str_p != Py_None) {
            if (key_is_int && value_is_int) {
                PyObject *format_str = PyUnicode_FromFormat("%ld: %ld, ", key_str_p, value_str_p);
                result = PyUnicode_Concat(result, format_str);
            }
            else if (key_is_int && !value_is_int) {
                PyObject *format_str = PyUnicode_FromFormat("%ld: \"%S\", ", key_str_p, value_str_p);
                result = PyUnicode_Concat(result, format_str);
            }
            else if (!key_is_int && value_is_int) {
                PyObject *format_str = PyUnicode_FromFormat("\"%S\": %ld, ", key_str_p, value_str_p);
                result = PyUnicode_Concat(result, format_str);

            } else {
                PyObject *format_str = PyUnicode_FromFormat("\"%S\": \"%S\", ", key_str_p, value_str_p);
                result = PyUnicode_Concat(result, format_str);

            }

        }
    }

    Py_ssize_t length = PyUnicode_GetLength(result);
    PyObject *new_result = PyUnicode_Substring(result, 0, length - 2);

    PyObject *format_str = PyUnicode_FromString("}");
    new_result = PyUnicode_Concat(new_result, format_str);


    return new_result;
}

static PyMethodDef methods[] = {
        {"loads", cjson_loads, METH_VARARGS, "Parse the json to dict"},
        {"dumps", cjson_dumps, METH_VARARGS, "convert dict to JSON"},
        {NULL, NULL, 0, NULL},
};

static PyModuleDef cjsonmodule = {
        PyModuleDef_HEAD_INIT,
        "cjson",
        "Module for parsing JSON with C API",
        -1,
        methods
};


PyMODINIT_FUNC PyInit_cjson(void)
{
    return PyModule_Create( &cjsonmodule);
};
