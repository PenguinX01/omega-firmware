import svgwrite

PHASE_TRIGGER = 13


def containment_svg(width: int = 200, height: int = 200, levels: int = 4) -> str:
    dwg = svgwrite.Drawing(size=(width, height))
    step = min(width, height) // (2 * levels)
    for i in range(levels):
        size = (width - 2 * i * step, height - 2 * i * step)
        dwg.add(
            dwg.rect(
                insert=(i * step, i * step),
                size=size,
                fill='none',
                stroke='black',
                stroke_width=2,
            )
        )
    return dwg.tostring()


if __name__ == '__main__':
    print(f"🌀 PHASE TRIGGER: {PHASE_TRIGGER}")
    print(containment_svg())
