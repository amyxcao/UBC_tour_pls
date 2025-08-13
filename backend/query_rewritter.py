from survey import Preferences


def generate_human_query(prefs: Preferences) -> str:
    parts = []

    # Color + material
    if prefs.colour and prefs.materiality:
        colour = ", ".join(prefs.colour).lower()
        material = ", ".join(prefs.materiality).lower()
        parts.append(f"{colour} {material} artifacts")
    elif prefs.materiality:
        material = ", ".join(prefs.materiality).lower()
        parts.append(f"{material} artifacts")
    elif prefs.colour:
        colour = ", ".join(prefs.colour).lower()
        parts.append(f"{colour} artifacts")
    else:
        parts.append("artifacts")

    # Time period
    if prefs.time_period:
        time = ", ".join(prefs.time_period)
        parts.append(
            f"from the {time} period{'s' if len(prefs.time_period) > 1 else ''}"
        )

    # Region
    if prefs.region:
        region = ", ".join(prefs.region)
        parts.append(f"originating in {region}")

    # Purpose
    purposes = [p.strip() for p in prefs.purpose if p.strip()]
    if purposes:
        parts.append(f"used for {', '.join(purposes)}")

    # Themes
    if prefs.themes:
        themes = ", ".join(prefs.themes).lower()
        parts.append(f"with themes of {themes}")

    # Additional interests
    extra = ""
    if prefs.additional_interests:
        extras = ", ".join(prefs.additional_interests).lower()
        extra = f" I also like {extras}."

    # Combine everything
    core = "I'm interested in " + ", ".join(parts).rstrip(",") + "."
    return core + extra
