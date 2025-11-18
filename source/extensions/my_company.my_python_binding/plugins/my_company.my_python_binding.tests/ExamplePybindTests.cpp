// Copyright (c) 2020-2021, NVIDIA CORPORATION. All rights reserved.
//
// NVIDIA CORPORATION and its licensors retain all intellectual property
// and proprietary rights in and to this software, related documentation
// and any modifications thereto.  Any use, reproduction, disclosure or
// distribution of this software and related documentation without an express
// license agreement from NVIDIA CORPORATION is strictly prohibited.
//

#include <my_company/my_python_binding/IMyCompanyMyPythonBindingInterface.h>
#include <my_company/my_python_binding/MyCompanyMyPythonBindingObject.h>

#include <doctest/doctest.h>

#include <carb/BindingsUtils.h>

CARB_BINDINGS("my_company.my_python_binding.tests")

namespace my_company::my_python_binding
{

class ExampleCppObject : public MyCompanyMyPythonBindingObject
{
public:
    static carb::ObjectPtr<IMyCompanyMyPythonBindingObjectInterface> create(const char* id)
    {
        return carb::stealObject<IMyCompanyMyPythonBindingObjectInterface>(new ExampleCppObject(id));
    }

    ExampleCppObject(const char* id)
        : MyCompanyMyPythonBindingObject(id)
    {
    }
};

class ExamplePybindTestFixture
{
public:
    static constexpr const char* k_registeredObjectId = "example_bound_object";

    ExamplePybindTestFixture()
        : m_exampleBoundInterface(carb::getCachedInterface<my_company::my_python_binding::IMyCompanyMyPythonBindingInterface>())
        , m_MyCompanyMyPythonBindingObject(ExampleCppObject::create(k_registeredObjectId))
    {
        m_exampleBoundInterface->registerMyCompanyMyPythonBindingObject(m_MyCompanyMyPythonBindingObject);
    }

    ~ExamplePybindTestFixture()
    {
        m_exampleBoundInterface->deregisterMyCompanyMyPythonBindingObject(m_MyCompanyMyPythonBindingObject);
    }

protected:
    IMyCompanyMyPythonBindingInterface* getExampleBoundInterface()
    {
        return m_exampleBoundInterface;
    }

    carb::ObjectPtr<IMyCompanyMyPythonBindingObjectInterface> getMyCompanyMyPythonBindingObject()
    {
        return m_MyCompanyMyPythonBindingObject;
    }

private:
    IMyCompanyMyPythonBindingInterface* m_exampleBoundInterface = nullptr;
    carb::ObjectPtr<IMyCompanyMyPythonBindingObjectInterface> m_MyCompanyMyPythonBindingObject;
};

}

TEST_SUITE("my_company.my_python_binding.tests")
{
    using namespace my_company::my_python_binding
;

    TEST_CASE_FIXTURE(ExamplePybindTestFixture, "Get Example Bound Interface")
    {
        CHECK(getExampleBoundInterface() != nullptr);
    }

    TEST_CASE_FIXTURE(ExamplePybindTestFixture, "Get Example Bound Object")
    {
        CHECK(getMyCompanyMyPythonBindingObject().get() != nullptr);
    }

    TEST_CASE_FIXTURE(ExamplePybindTestFixture, "Find Example Bound Object")
    {
        SUBCASE("Registered")
        {
            carb::ObjectPtr<IMyCompanyMyPythonBindingObjectInterface> foundObject = getExampleBoundInterface()->findMyCompanyMyPythonBindingObject(k_registeredObjectId);
            CHECK(foundObject.get() == getMyCompanyMyPythonBindingObject().get());
            CHECK(foundObject.get() != nullptr);
        }

        SUBCASE("Unregistered")
        {
            carb::ObjectPtr<IMyCompanyMyPythonBindingObjectInterface> foundObject = getExampleBoundInterface()->findMyCompanyMyPythonBindingObject("unregistered_object_id");
            CHECK(foundObject.get() != getMyCompanyMyPythonBindingObject().get());
            CHECK(foundObject.get() == nullptr);
        }
    }
}
