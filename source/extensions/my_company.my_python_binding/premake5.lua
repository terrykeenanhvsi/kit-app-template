-- Setup the extension.
local ext = get_current_extension_info()
project_ext(ext)

-- Link folders that should be packaged with the extension.
repo_build.prebuild_link {
    { "data", ext.target_dir.."/data" },
    { "docs", ext.target_dir.."/docs" },
}

-- Build the C++ plugin that will be loaded by the extension.
project_ext_plugin(ext, "my_company.my_python_binding.plugin")
    add_files("include", "include/my_company/my_python_binding")
    add_files("source", "plugins/my_company.my_python_binding")
    includedirs { "include", "plugins/my_company.my_python_binding" }

-- Build Python bindings that will be loaded by the extension.
project_ext_bindings {
    ext = ext,
    project_name = "my_company.my_python_binding.python",
    module = "_my_company_my_python_binding_lib",
    src = "bindings/python/my_company.my_python_binding",
    target_subdir = "my_company/my_python_binding"
}
    includedirs { "include" }
    repo_build.prebuild_link {
        { "python/impl", ext.target_dir.."/my_company/my_python_binding/impl" },
        { "python/tests", ext.target_dir.."/my_company/my_python_binding/tests" },
    }

-- Build the C++ plugin that will be loaded by the tests.
project_ext_tests(ext, "my_company.my_python_binding.tests")
    add_files("source", "plugins/my_company.my_python_binding.tests")
    includedirs { "include", "plugins/my_company.my_python_binding.tests", "%{target_deps}/doctest/include" }
