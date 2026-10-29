# Load the debug and release variables
file(GLOB DATA_FILES "${CMAKE_CURRENT_LIST_DIR}/iceoryx2-*-data.cmake")

foreach(f ${DATA_FILES})
    include(${f})
endforeach()

# Create the targets for all the components
foreach(_COMPONENT ${iceoryx2_COMPONENT_NAMES} )
    if(NOT TARGET ${_COMPONENT})
        add_library(${_COMPONENT} INTERFACE IMPORTED)
        message(${iceoryx2_MESSAGE_MODE} "Conan: Component target declared '${_COMPONENT}'")
    endif()
endforeach()

if(NOT TARGET iceoryx2::iceoryx2)
    add_library(iceoryx2::iceoryx2 INTERFACE IMPORTED)
    message(${iceoryx2_MESSAGE_MODE} "Conan: Target declared 'iceoryx2::iceoryx2'")
endif()
# Load the debug and release library finders
file(GLOB CONFIG_FILES "${CMAKE_CURRENT_LIST_DIR}/iceoryx2-Target-*.cmake")

foreach(f ${CONFIG_FILES})
    include(${f})
endforeach()