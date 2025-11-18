// Copyright (c) 2022, NVIDIA CORPORATION. All rights reserved.
//
// NVIDIA CORPORATION and its licensors retain all intellectual property
// and proprietary rights in and to this software, related documentation
// and any modifications thereto.  Any use, reproduction, disclosure or
// distribution of this software and related documentation without an express
// license agreement from NVIDIA CORPORATION is strictly prohibited.
//

#define CARB_EXPORTS

#include <carb/PluginUtils.h>

#include <omni/ext/IExt.h>

#include <my_company/my_python_binding/IMyCompanyMyPythonBindingInterface.h>

#include <unordered_map>

const struct carb::PluginImplDesc pluginImplDesc = { "my_company.my_python_binding.plugin",
                                                     "An example C++ extension.", "NVIDIA",
                                                     carb::PluginHotReload::eEnabled, "dev" };

namespace my_company::my_python_binding
{

class ExampleBoundImplementation : public IMyCompanyMyPythonBindingInterface
{
public:
    void registerMyCompanyMyPythonBindingObject(carb::ObjectPtr<IMyCompanyMyPythonBindingObjectInterface>& object) override
    {
        if (object)
        {
            m_registeredObjectsById[object->getId()] = object;
        }
    }

    void deregisterMyCompanyMyPythonBindingObject(carb::ObjectPtr<IMyCompanyMyPythonBindingObjectInterface>& object) override
    {
        if (object)
        {
            const auto& it = m_registeredObjectsById.find(object->getId());
            if (it != m_registeredObjectsById.end())
            {
                m_registeredObjectsById.erase(it);
            }
        }
    }

    carb::ObjectPtr<IMyCompanyMyPythonBindingObjectInterface> findMyCompanyMyPythonBindingObject(const char* id) const override
    {
        const auto& it = m_registeredObjectsById.find(id);
        if (it != m_registeredObjectsById.end())
        {
            return it->second;
        }

        return carb::ObjectPtr<IMyCompanyMyPythonBindingObjectInterface>();
    }

private:
    std::unordered_map<std::string, carb::ObjectPtr<IMyCompanyMyPythonBindingObjectInterface>> m_registeredObjectsById;
};

}

CARB_PLUGIN_IMPL(pluginImplDesc, my_company::my_python_binding::ExampleBoundImplementation)

void fillInterface(my_company::my_python_binding::ExampleBoundImplementation& iface)
{
}
