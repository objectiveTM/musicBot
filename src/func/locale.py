import nextcord

def locale(ko , en) -> dict[nextcord.Locale]:
    loc:nextcord.Locale = nextcord.Locale

    rmxDict = {
        loc.en_GB: en,
        loc.en_US: en,
        loc.ko: ko
    }

    return rmxDict
