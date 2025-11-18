// Copyright (c) 2022, NVIDIA CORPORATION. All rights reserved.
//
// NVIDIA CORPORATION and its licensors retain all intellectual property
// and proprietary rights in and to this software, related documentation
// and any modifications thereto.  Any use, reproduction, disclosure or
// distribution of this software and related documentation without an express
// license agreement from NVIDIA CORPORATION is strictly prohibited.
//
#pragma once

#include <my_company/my_python_binding/IMyCompanyMyPythonBindingObjectInterface.h>

#include <carb/ObjectUtils.h>

#include <omni/String.h>

namespace my_company::my_python_binding
{

/**
 * Helper base class for bound object implementations.
 */
class MyCompanyMyPythonBindingObject : public IMyCompanyMyPythonBindingObjectInterface
{
    CARB_IOBJECT_IMPL

public:
    /**
     * Constructor.
     *
     * @param id Id of the bound object.
     */
    MyCompanyMyPythonBindingObject(const char* id)
        : m_id(id ? id : "")
    {
    }

    /**
     * @ref IMyCompanyMyPythonBindingObjectInterface::getId
     */
    const char* getId() const override
    {
        return m_id.c_str();
    }

protected:
    const omni::string m_id; //!< Id of the bound object.
};

}
