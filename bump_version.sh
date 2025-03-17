uv run task version neonize --last
uv run task version goneonize --last
if [[ $VERSION_MAJOR == "true" ]];then
    uv run task version update major
elif [[ $VERSION_MINOR == "true" ]];then
    uv run task version update minor
elif [[ $VERSION_PATCH == "true" ]];then
    uv run task version update patch
elif [[ ( $VERSION_MAJOR == "false" && $VERSION_MINOR == "false" && $VERSION_PATCH == "false" && $VERSION_POST == "false" ) || $VERSION_POST == "true" ]]; then
    uv run task version update post
fi