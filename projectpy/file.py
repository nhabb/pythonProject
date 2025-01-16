from tabulate import tabulate

help(tabulate)

def tabulate(
    tabular_data: Mapping[str, Iterable[Any]] | Iterable[Iterable[Any]],
    headers: str | dict[str, str] | Sequence[str] = (),
    tablefmt: str | TableFormat = "simple",
    floatfmt: str | Iterable[str] = "g",
    intfmt: str | Iterable[str] = "",
    numalign: str | None = "default",
    stralign: str | None = "default",
    missingval: str | Iterable[str] = "",
    showindex: str | bool | Iterable[Any] = "default",
    disable_numparse: bool | Iterable[int] = False,
    colalign: Iterable[str | None] | None = None,
    maxcolwidths: int | Iterable[int | None] | None = None,
    rowalign: str | Iterable[str] | None = None,
    maxheadercolwidths: int | Iterable[int] | None = None,
) -> str: ...


    print( "\n" , tabulate( courses[1:] , courses[0] , tablefmt = "github" ) , "\n" , sep = "" )
