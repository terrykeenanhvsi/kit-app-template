// Copyright (c) 2022, NVIDIA CORPORATION. All rights reserved.
//
// NVIDIA CORPORATION and its licensors retain all intellectual property
// and proprietary rights in and to this software, related documentation
// and any modifications thereto.  Any use, reproduction, disclosure or
// distribution of this software and related documentation without an express
// license agreement from NVIDIA CORPORATION is strictly prohibited.
//

#include <carb/BindingsPythonUtils.h>

#include <my_company/my_python_binding/MyCompanyMyPythonBindingObject.h>
#include <my_company/my_python_binding/IMyCompanyMyPythonBindingInterface.h>

#include <string>

CARB_BINDINGS("my_company.my_python_binding.python")

DISABLE_PYBIND11_DYNAMIC_CAST(my_company::my_python_binding::IMyCompanyMyPythonBindingInterface)
DISABLE_PYBIND11_DYNAMIC_CAST(my_company::my_python_binding::IMyCompanyMyPythonBindingObjectInterface)

namespace
{

/**
 * Concrete bound object class that will be reflected to Python.
 */
class PythonMyCompanyMyPythonBindingObject : public my_company::my_python_binding::MyCompanyMyPythonBindingObject
{
public:
    /**
     * Factory.
     *
     * @param id Id of the bound action.
     *
     * @return The bound object that was created.
     */
    static carb::ObjectPtr<PythonMyCompanyMyPythonBindingObject> create(const char* id)
    {
        // Note: It is important to construct the handler using ObjectPtr<T>::InitPolicy::eSteal,
        // otherwise we end up incresing the reference count by one too many during construction,
        // resulting in carb::ObjectPtr<T> instance whose wrapped object will never be destroyed.
        return carb::stealObject<PythonMyCompanyMyPythonBindingObject>(new PythonMyCompanyMyPythonBindingObject(id));
    }

    /**
     * Constructor.
     *
     * @param id Id of the bound object.
     */
    PythonMyCompanyMyPythonBindingObject(const char* id)
        : MyCompanyMyPythonBindingObject(id)
        , m_memberInt(0)
        , m_memberBool(false)
        , m_memberString()
    {
    }

    // To deomnstrate binding a fuction that accepts an argument.
    void multiplyIntProperty(int value)
    {
        m_memberInt *= value;
    }

    // To deomnstrate binding a fuction that returns a value.
    bool toggleBoolProperty()
    {
        m_memberBool = !m_memberBool;
        return m_memberBool;
    }

    // To deomnstrate binding a fuction that accepts an argument and returns a value.
    const char* appendStringProperty(const char* value)
    {
        m_memberString += value;
        return m_memberString.c_str();
    }

    // To deomnstrate binding properties using accessors.
    const char* getMemberString() const
    {
        return m_memberString.c_str();
    }

    // To deomnstrate binding properties using accessors.
    void setMemberString(const char* value)
    {
        m_memberString = value;
    }

    // To deomnstrate binding properties directly.
    int m_memberInt;
    bool m_memberBool;

private:
    // To deomnstrate binding properties using accessors.
    std::string m_memberString;
};

// Define the pybind11 module using the same name specified in premake5.lua
PYBIND11_MODULE(_my_company_my_python_binding_lib, m)
{
    using namespace my_company::my_python_binding
;

    m.doc() = "pybind11 my_company.my_python_binding bindings";

    carb::defineInterfaceClass<IMyCompanyMyPythonBindingInterface>(
        m, "IMyCompanyMyPythonBindingInterface", "acquire_bound_interface", "release_bound_interface")
        .def("register_bound_object", &IMyCompanyMyPythonBindingInterface::registerMyCompanyMyPythonBindingObject,
             R"(
             Register a bound object.

             Args:
                 object: The bound object to register.
             )",
             py::arg("object"))
        .def("deregister_bound_object", &IMyCompanyMyPythonBindingInterface::deregisterMyCompanyMyPythonBindingObject,
             R"(
             Deregister a bound object.

             Args:
                 object: The bound object to deregister.
             )",
             py::arg("object"))
        .def("find_bound_object", &IMyCompanyMyPythonBindingInterface::findMyCompanyMyPythonBindingObject, py::return_value_policy::reference,
             R"(
             Find a bound object.

             Args:
                 id: Id of the bound object.

             Return:
                 The bound object if it exists, an empty object otherwise.
             )",
             py::arg("id"))
        /**/;

    py::class_<IMyCompanyMyPythonBindingObjectInterface, carb::ObjectPtr<IMyCompanyMyPythonBindingObjectInterface>>(m, "IMyCompanyMyPythonBindingObjectInterface")
        .def_property_readonly("id", &IMyCompanyMyPythonBindingObjectInterface::getId, py::return_value_policy::reference,
            R"(
             Get the id of this bound object.

             Return:
                 The id of this bound object.
             )")
        /**/;

    py::class_<PythonMyCompanyMyPythonBindingObject, IMyCompanyMyPythonBindingObjectInterface, carb::ObjectPtr<PythonMyCompanyMyPythonBindingObject>>(m, "MyCompanyMyPythonBindingObject")
        .def(py::init([](const char* id) { return PythonMyCompanyMyPythonBindingObject::create(id); }),
             R"(
             Create a bound object.

             Args:
                 id: Id of the bound object.

             Return:
                 The bound object that was created.
             )",
             py::arg("id"))
        .def_readwrite("property_int", &PythonMyCompanyMyPythonBindingObject::m_memberInt,
             R"(
             Int property bound directly.
             )")
        .def_readwrite("property_bool", &PythonMyCompanyMyPythonBindingObject::m_memberBool,
             R"(
             Bool property bound directly.
             )")
        .def_property("property_string", &PythonMyCompanyMyPythonBindingObject::getMemberString, &PythonMyCompanyMyPythonBindingObject::setMemberString, py::return_value_policy::reference,
             R"(
             String property bound using accessors.
             )")
        .def("multiply_int_property", &PythonMyCompanyMyPythonBindingObject::multiplyIntProperty,
             R"(
             Bound fuction that accepts an argument.

             Args:
                 value_to_multiply: The value to multiply by.
             )",
             py::arg("value_to_multiply"))
        .def("toggle_bool_property", &PythonMyCompanyMyPythonBindingObject::toggleBoolProperty,
             R"(
             Bound fuction that returns a value.

             Return:
                 The toggled bool value.
             )")
        .def("append_string_property", &PythonMyCompanyMyPythonBindingObject::appendStringProperty, py::return_value_policy::reference,
             R"(
             Bound fuction that accepts an argument and returns a value.

             Args:
                 value_to_append: The value to append.

             Return:
                 The new string value.
             )",
             py::arg("value_to_append"))
        /**/;
}
}
