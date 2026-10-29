script_folder="/home/ecku/develop/recipes/conan-iceoryx2/test_package/build/gcc-13-x86_64-20-release/generators"
echo "echo Restoring environment" > "$script_folder/deactivate_conanrunenv-release-x86_64.sh"
for v in LD_LIBRARY_PATH DYLD_LIBRARY_PATH
do
   is_defined="true"
   value=$(printenv $v) || is_defined="" || true
   if [ -n "$value" ] || [ -n "$is_defined" ]
   then
       echo export "$v='$value'" >> "$script_folder/deactivate_conanrunenv-release-x86_64.sh"
   else
       echo unset $v >> "$script_folder/deactivate_conanrunenv-release-x86_64.sh"
   fi
done

export LD_LIBRARY_PATH="/home/ecku/.conan2/p/b/iceor93aea0772d84b/p/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
export DYLD_LIBRARY_PATH="/home/ecku/.conan2/p/b/iceor93aea0772d84b/p/lib${DYLD_LIBRARY_PATH:+:$DYLD_LIBRARY_PATH}"