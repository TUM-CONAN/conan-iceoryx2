########### AGGREGATED COMPONENTS AND DEPENDENCIES FOR THE MULTI CONFIG #####################
#############################################################################################

set(iceoryx2_COMPONENT_NAMES "")
if(DEFINED iceoryx2_FIND_DEPENDENCY_NAMES)
  list(APPEND iceoryx2_FIND_DEPENDENCY_NAMES )
  list(REMOVE_DUPLICATES iceoryx2_FIND_DEPENDENCY_NAMES)
else()
  set(iceoryx2_FIND_DEPENDENCY_NAMES )
endif()

########### VARIABLES #######################################################################
#############################################################################################
set(iceoryx2_PACKAGE_FOLDER_RELEASE "/home/ecku/.conan2/p/b/iceor93aea0772d84b/p")
set(iceoryx2_BUILD_MODULES_PATHS_RELEASE )


set(iceoryx2_INCLUDE_DIRS_RELEASE "${iceoryx2_PACKAGE_FOLDER_RELEASE}/include"
			"${iceoryx2_PACKAGE_FOLDER_RELEASE}/include/iceoryx2/v0.9.3")
set(iceoryx2_RES_DIRS_RELEASE )
set(iceoryx2_DEFINITIONS_RELEASE )
set(iceoryx2_SHARED_LINK_FLAGS_RELEASE )
set(iceoryx2_EXE_LINK_FLAGS_RELEASE )
set(iceoryx2_OBJECTS_RELEASE )
set(iceoryx2_COMPILE_DEFINITIONS_RELEASE )
set(iceoryx2_COMPILE_OPTIONS_C_RELEASE )
set(iceoryx2_COMPILE_OPTIONS_CXX_RELEASE )
set(iceoryx2_LIB_DIRS_RELEASE "${iceoryx2_PACKAGE_FOLDER_RELEASE}/lib")
set(iceoryx2_BIN_DIRS_RELEASE "${iceoryx2_PACKAGE_FOLDER_RELEASE}/bin")
set(iceoryx2_LIBRARY_TYPE_RELEASE SHARED)
set(iceoryx2_IS_HOST_WINDOWS_RELEASE 0)
set(iceoryx2_LIBS_RELEASE iceoryx2_ffi_c iceoryx2_cxx)
set(iceoryx2_SYSTEM_LIBS_RELEASE )
set(iceoryx2_FRAMEWORK_DIRS_RELEASE )
set(iceoryx2_FRAMEWORKS_RELEASE )
set(iceoryx2_BUILD_DIRS_RELEASE "${iceoryx2_PACKAGE_FOLDER_RELEASE}/lib/cmake")
set(iceoryx2_NO_SONAME_MODE_RELEASE FALSE)


# COMPOUND VARIABLES
set(iceoryx2_COMPILE_OPTIONS_RELEASE)
if (NOT "${iceoryx2_COMPILE_OPTIONS_CXX_RELEASE}" STREQUAL "")
    list(APPEND iceoryx2_COMPILE_OPTIONS_RELEASE
        "$<$<COMPILE_LANGUAGE:CXX>:${iceoryx2_COMPILE_OPTIONS_CXX_RELEASE}>")
endif ()
if (NOT "${iceoryx2_COMPILE_OPTIONS_C_RELEASE}" STREQUAL "")
    list(APPEND iceoryx2_COMPILE_OPTIONS_RELEASE
        "$<$<COMPILE_LANGUAGE:C>:${iceoryx2_COMPILE_OPTIONS_C_RELEASE}>")
endif ()
set(iceoryx2_LINKER_FLAGS_RELEASE)
if (NOT "${iceoryx2_SHARED_LINK_FLAGS_RELEASE}" STREQUAL "")
    list(APPEND iceoryx2_LINKER_FLAGS_RELEASE
        "$<$<OR:$<STREQUAL:$<TARGET_PROPERTY:TYPE>,SHARED_LIBRARY>,$<STREQUAL:$<TARGET_PROPERTY:TYPE>,MODULE_LIBRARY>>:${iceoryx2_SHARED_LINK_FLAGS_RELEASE}>")
endif ()
if (NOT "${iceoryx2_EXE_LINK_FLAGS_RELEASE}" STREQUAL "")
    list(APPEND iceoryx2_LINKER_FLAGS_RELEASE
        "$<$<STREQUAL:$<TARGET_PROPERTY:TYPE>,EXECUTABLE>:${iceoryx2_EXE_LINK_FLAGS_RELEASE}>")
endif ()


set(iceoryx2_COMPONENTS_RELEASE )