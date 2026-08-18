param(
    [Parameter(Position = 0)]
    [ValidateSet("check", "synthetic", "real")]
    [string] $Command = "check",

    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]] $Arguments
)

$env:PYTHONPATH = "$PSScriptRoot\src"
python -m esm2_fitness.pipeline $Command @Arguments
exit $LASTEXITCODE
