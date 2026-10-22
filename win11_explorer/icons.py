"""
Windows 11 Fluent Icon provider for Win11 Explorer.
Provides crisp, vector-based Fluent Design 2 icons rendered via SVG.
"""

from PyQt6.QtGui import QIcon, QPixmap, QPainter, QColor
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtCore import QByteArray, QSize, Qt

SVGS = {
    # Windows 11 Authentic Fluent Folder
    "folder": """<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <linearGradient id="backGrad" x1="4" y1="7" x2="4" y2="41" gradientUnits="userSpaceOnUse">
                <stop offset="0%" stop-color="#EAA600"/>
                <stop offset="100%" stop-color="#C68400"/>
            </linearGradient>
            <linearGradient id="frontGrad" x1="4" y1="15" x2="4" y2="41" gradientUnits="userSpaceOnUse">
                <stop offset="0%" stop-color="#FFE464"/>
                <stop offset="30%" stop-color="#FFD13B"/>
                <stop offset="100%" stop-color="#FFB900"/>
            </linearGradient>
            <linearGradient id="sheetGrad" x1="8" y1="11" x2="40" y2="20" gradientUnits="userSpaceOnUse">
                <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0.8"/>
                <stop offset="100%" stop-color="#E1DFDD" stop-opacity="0.5"/>
            </linearGradient>
        </defs>
        <!-- Back Folder Flap -->
        <path d="M4 11C4 8.79086 5.79086 7 8 7H18.5C19.8 7 21 7.6 21.8 8.6L24.8 12.2C25.4 12.7 26.2 13 27 13H40C42.2091 13 44 14.7909 44 17V37C44 39.2091 42.2091 41 40 41H8C5.79086 41 4 39.2091 4 37V11Z" fill="url(#backGrad)"/>
        <!-- Sheet Preview inside folder -->
        <rect x="7" y="11" width="34" height="10" rx="2" fill="url(#sheetGrad)"/>
        <!-- Front Folder Pocket with Fluent 3D curve -->
        <path d="M4 17C4 15.3431 5.34315 14 7 14H41C42.6569 14 44 15.3431 44 17V37C44 39.2091 42.2091 41 40 41H8C5.79086 41 4 39.2091 4 37V17Z" fill="url(#frontGrad)"/>
        <!-- Top highlight line on front pocket -->
        <path d="M7 14.5H41C42.3807 14.5 43.5 15.6193 43.5 17V18C43.5 16.6193 42.3807 15.5 41 15.5H7C5.61929 15.5 4.5 16.6193 4.5 18V17C4.5 15.6193 5.61929 14.5 7 14.5Z" fill="#FFF6C2" fill-opacity="0.7"/>
    </svg>""",

    # Desktop folder
    "folder-desktop": """<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect x="5" y="7" width="38" height="26" rx="4" fill="#0078D4"/>
        <rect x="7" y="9" width="34" height="22" rx="2.5" fill="#2B88D8"/>
        <!-- Desktop Wallpaper Preview -->
        <path d="M7 23L16 15L25 23H7Z" fill="#60CDFF" opacity="0.6"/>
        <path d="M21 23L28 17L37 25H21Z" fill="#C7E0F4" opacity="0.8"/>
        <rect x="22" y="33" width="4" height="7" rx="1" fill="#005A9E"/>
        <rect x="14" y="40" width="20" height="3" rx="1.5" fill="#0078D4"/>
    </svg>""",

    # Downloads folder
    "folder-downloads": """<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
        <!-- Base Yellow Folder -->
        <path d="M4 11C4 8.79 5.79 7 8 7H18.5C19.8 7 21 7.6 21.8 8.6L24.8 12.2C25.4 12.7 26.2 13 27 13H40C42.21 13 44 14.79 44 17V37C44 39.21 42.21 41 40 41H8C5.79 41 4 39.21 4 37V11Z" fill="#EAA600"/>
        <path d="M4 17C4 15.34 5.34 14 7 14H41C42.66 14 44 15.34 44 17V37C44 39.21 42.21 41 40 41H8C5.79 41 4 39.21 4 37V17Z" fill="#FFC828"/>
        <!-- Download Circle Badge -->
        <circle cx="24" cy="27" r="11" fill="#0078D4"/>
        <path d="M24 19V30M24 30L19.5 25.5M24 30L28.5 25.5" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
        <path d="M19 33.5H29" stroke="white" stroke-width="2.5" stroke-linecap="round"/>
    </svg>""",

    # Documents folder
    "folder-documents": """<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M4 11C4 8.79 5.79 7 8 7H18.5C19.8 7 21 7.6 21.8 8.6L24.8 12.2C25.4 12.7 26.2 13 27 13H40C42.21 13 44 14.79 44 17V37C44 39.21 42.21 41 40 41H8C5.79 41 4 39.21 4 37V11Z" fill="#EAA600"/>
        <path d="M4 17C4 15.34 5.34 14 7 14H41C42.66 14 44 15.34 44 17V37C44 39.21 42.21 41 40 41H8C5.79 41 4 39.21 4 37V17Z" fill="#FFC828"/>
        <!-- Document Sheet -->
        <rect x="15" y="19" width="18" height="20" rx="2" fill="#FFFFFF"/>
        <rect x="18" y="23" width="12" height="2" rx="1" fill="#0078D4"/>
        <rect x="18" y="27" width="12" height="2" rx="1" fill="#90C4F5"/>
        <rect x="18" y="31" width="8" height="2" rx="1" fill="#90C4F5"/>
        <rect x="18" y="35" width="10" height="2" rx="1" fill="#C0DEFB"/>
    </svg>""",

    # Pictures folder
    "folder-pictures": """<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M4 11C4 8.79 5.79 7 8 7H18.5C19.8 7 21 7.6 21.8 8.6L24.8 12.2C25.4 12.7 26.2 13 27 13H40C42.21 13 44 14.79 44 17V37C44 39.21 42.21 41 40 41H8C5.79 41 4 39.21 4 37V11Z" fill="#EAA600"/>
        <path d="M4 17C4 15.34 5.34 14 7 14H41C42.66 14 44 15.34 44 17V37C44 39.21 42.21 41 40 41H8C5.79 41 4 39.21 4 37V17Z" fill="#FFC828"/>
        <!-- Photo Card -->
        <rect x="14" y="19" width="20" height="19" rx="2" fill="#107C41"/>
        <circle cx="19" cy="24" r="2.2" fill="#FFEB80"/>
        <path d="M14 33L21 26L26 31L29 28L34 33.5V36C34 37.1 33.1 38 32 38H16C14.9 38 14 37.1 14 36V33Z" fill="#81C784"/>
    </svg>""",

    # Music folder
    "folder-music": """<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M4 11C4 8.79 5.79 7 8 7H18.5C19.8 7 21 7.6 21.8 8.6L24.8 12.2C25.4 12.7 26.2 13 27 13H40C42.21 13 44 14.79 44 17V37C44 39.21 42.21 41 40 41H8C5.79 41 4 39.21 4 37V11Z" fill="#EAA600"/>
        <path d="M4 17C4 15.34 5.34 14 7 14H41C42.66 14 44 15.34 44 17V37C44 39.21 42.21 41 40 41H8C5.79 41 4 39.21 4 37V17Z" fill="#FFC828"/>
        <!-- Orange/Red Music Disc Badge -->
        <circle cx="24" cy="28" r="11" fill="#E84D23"/>
        <path d="M22 23V31M22 31C22 32.1 21.1 33 20 33C18.9 33 18 32.1 18 31C18 29.9 18.9 29 20 29C20.4 29 20.7 29.1 21 29.3V23L27 21.5V29M27 29C27 30.1 26.1 31 25 31C23.9 31 23 30.1 23 29C23 27.9 23.9 27 25 27C25.4 27 25.7 27.1 26 27.3V21.5L22 23Z" fill="white"/>
    </svg>""",

    # Videos folder
    "folder-videos": """<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M4 11C4 8.79 5.79 7 8 7H18.5C19.8 7 21 7.6 21.8 8.6L24.8 12.2C25.4 12.7 26.2 13 27 13H40C42.21 13 44 14.79 44 17V37C44 39.21 42.21 41 40 41H8C5.79 41 4 39.21 4 37V11Z" fill="#EAA600"/>
        <path d="M4 17C4 15.34 5.34 14 7 14H41C42.66 14 44 15.34 44 17V37C44 39.21 42.21 41 40 41H8C5.79 41 4 39.21 4 37V17Z" fill="#FFC828"/>
        <!-- Purple Film Clapperboard -->
        <rect x="14" y="20" width="20" height="16" rx="3" fill="#8764B8"/>
        <path d="M22 24.5L28 28L22 31.5V24.5Z" fill="white"/>
    </svg>""",

    # Home / User Folder
    "folder-home": """<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M24 6L6 21H11V39C11 40.1 11.9 41 13 41H20V30C20 28.9 20.9 28 22 28H26C27.1 28 28 28.9 28 30V41H35C36.1 41 37 40.1 37 39V21H42L24 6Z" fill="#0078D4"/>
    </svg>""",

    # This PC / Computer
    "this-pc": """<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect x="6" y="8" width="36" height="24" rx="3" fill="#0078D4"/>
        <rect x="8" y="10" width="32" height="20" rx="2" fill="#E1DFDD"/>
        <rect x="22" y="32" width="4" height="6" fill="#8A8886"/>
        <path d="M14 38H34C35.1 38 36 38.9 36 40V41H12V40C12 38.9 12.9 38 14 38Z" fill="#605E5C"/>
        <circle cx="24" cy="20" r="4" fill="#0078D4"/>
    </svg>""",

    # Hard Drive with activity & capacity
    "drive": """<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect x="6" y="12" width="36" height="24" rx="4" fill="#E1DFDD"/>
        <rect x="8" y="14" width="32" height="20" rx="2.5" fill="#FAF9F8"/>
        <!-- Drive bay lines -->
        <line x1="12" y1="20" x2="30" y2="20" stroke="#8A8886" stroke-width="1.5" stroke-linecap="round"/>
        <!-- Capacity Bar -->
        <rect x="12" y="27" width="24" height="3" rx="1.5" fill="#C8C6C4"/>
        <rect x="12" y="27" width="16" height="3" rx="1.5" fill="#0078D4"/>
        <!-- Activity LED -->
        <circle cx="36" cy="18" r="1.5" fill="#107C41"/>
    </svg>""",

    # Recycle Bin
    "trash": """<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M12 14L15 39C15.2 40.7 16.6 42 18.3 42H29.7C31.4 42 32.8 40.7 33 39L36 14H12Z" fill="#2B88D8"/>
        <rect x="10" y="9" width="28" height="4" rx="2" fill="#0078D4"/>
        <rect x="20" y="6" width="8" height="3" rx="1.5" fill="#005A9E"/>
        <path d="M21 21L24 18L27 21M24 19V28M24 28L21 25M24 28L27 25" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>""",

    # Network
    "network": """<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="24" cy="24" r="16" stroke="#0078D4" stroke-width="3" fill="none"/>
        <ellipse cx="24" cy="24" rx="8" ry="16" stroke="#0078D4" stroke-width="2" fill="none"/>
        <line x1="8" y1="24" x2="40" y2="24" stroke="#0078D4" stroke-width="2"/>
    </svg>""",

    # Navigation: Back
    "nav-back": """<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M15 19L8 12L15 5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>""",

    # Navigation: Forward
    "nav-forward": """<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M9 5L16 12L9 19" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>""",

    # Navigation: Up
    "nav-up": """<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M12 19V5M12 5L6 11M12 5L18 11" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>""",

    # Navigation: Refresh
    "refresh": """<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M19 12A7 7 0 1 1 17.5 7.4L20 5V10H15L17 8A5 5 0 1 0 17 12H19Z" fill="currentColor"/>
    </svg>""",

    # Caption: Minimize (─)
    "cap-min": """<svg viewBox="0 0 12 12" fill="none" xmlns="http://www.w3.org/2000/svg">
        <line x1="1" y1="6" x2="11" y2="6" stroke="currentColor" stroke-width="1.2"/>
    </svg>""",

    # Caption: Maximize (□)
    "cap-max": """<svg viewBox="0 0 12 12" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect x="1.5" y="1.5" width="9" height="9" stroke="currentColor" stroke-width="1.2"/>
    </svg>""",

    # Caption: Restore (❐)
    "cap-restore": """<svg viewBox="0 0 12 12" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M3.5 3.5V1.5H10.5V8.5H8.5" stroke="currentColor" stroke-width="1.1"/>
        <rect x="1.5" y="3.5" width="7" height="7" stroke="currentColor" stroke-width="1.1"/>
    </svg>""",

    # Caption: Close (✕)
    "cap-close": """<svg viewBox="0 0 12 12" fill="none" xmlns="http://www.w3.org/2000/svg">
        <line x1="1.5" y1="1.5" x2="10.5" y2="10.5" stroke="currentColor" stroke-width="1.2"/>
        <line x1="10.5" y1="1.5" x2="1.5" y2="10.5" stroke="currentColor" stroke-width="1.2"/>
    </svg>""",

    # Command Bar: New with circle plus
    "new": """<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="12" cy="12" r="9" fill="#0078D4"/>
        <path d="M12 8V16M8 12H16" stroke="white" stroke-width="2.2" stroke-linecap="round"/>
    </svg>""",

    # Command Bar: Cut
    "cut": """<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="6" cy="18" r="3" stroke="currentColor" stroke-width="2"/>
        <circle cx="6" cy="6" r="3" stroke="currentColor" stroke-width="2"/>
        <path d="M8.5 16.5L19 6M8.5 7.5L19 18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
    </svg>""",

    # Command Bar: Copy
    "copy": """<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect x="8" y="8" width="12" height="13" rx="2" stroke="currentColor" stroke-width="2"/>
        <path d="M16 8V5C16 3.9 15.1 3 14 3H5C3.9 3 3 3.9 3 5V14C3 15.1 3.9 16 5 16H8" stroke="currentColor" stroke-width="2"/>
    </svg>""",

    # Command Bar: Paste
    "paste": """<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect x="5" y="6" width="14" height="15" rx="2" stroke="currentColor" stroke-width="2"/>
        <rect x="9" y="3" width="6" height="4" rx="1.5" fill="currentColor"/>
    </svg>""",

    # Command Bar: Rename
    "rename": """<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M4 20H8L18.5 9.5C19.3 8.7 19.3 7.3 18.5 6.5L16.5 4.5C15.7 3.7 14.3 3.7 13.5 4.5L3 15V20H4Z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>
        <path d="M12.5 5.5L17.5 10.5" stroke="currentColor" stroke-width="2"/>
    </svg>""",

    # Command Bar: Share
    "share": """<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="18" cy="5" r="3" stroke="currentColor" stroke-width="2"/>
        <circle cx="6" cy="12" r="3" stroke="currentColor" stroke-width="2"/>
        <circle cx="18" cy="19" r="3" stroke="currentColor" stroke-width="2"/>
        <path d="M8.6 13.5L15.4 17.5M15.4 6.5L8.6 10.5" stroke="currentColor" stroke-width="2"/>
    </svg>""",

    # Command Bar: Delete
    "delete": """<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M3 6H21M8 6V4C8 3.4 8.4 3 9 3H15C15.6 3 16 3.4 16 4V6M19 6V20C19 20.6 18.6 21 18 21H6C5.4 21 5 20.6 5 20V6H19Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        <line x1="10" y1="10" x2="10" y2="17" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
        <line x1="14" y1="10" x2="14" y2="17" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
    </svg>""",

    # Command Bar: Sort
    "sort": """<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M4 6H13M4 12H10M4 18H7" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
        <path d="M16 9L19 6L22 9M19 6V18" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>""",

    # Command Bar: View
    "view": """<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect x="3" y="3" width="7" height="7" rx="1.5" stroke="currentColor" stroke-width="2"/>
        <rect x="14" y="3" width="7" height="7" rx="1.5" stroke="currentColor" stroke-width="2"/>
        <rect x="3" y="14" width="7" height="7" rx="1.5" stroke="currentColor" stroke-width="2"/>
        <rect x="14" y="14" width="7" height="7" rx="1.5" stroke="currentColor" stroke-width="2"/>
    </svg>""",

    # Command Bar: Details Pane Toggle
    "details-pane": """<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect x="3" y="3" width="18" height="18" rx="2" stroke="currentColor" stroke-width="2"/>
        <line x1="15" y1="3" x2="15" y2="21" stroke="currentColor" stroke-width="2"/>
        <circle cx="18" cy="7" r="1.5" fill="currentColor"/>
    </svg>""",

    # Command Bar: More
    "more": """<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="5" cy="12" r="2" fill="currentColor"/>
        <circle cx="12" cy="12" r="2" fill="currentColor"/>
        <circle cx="19" cy="12" r="2" fill="currentColor"/>
    </svg>""",

    # Search Magnifying Glass
    "search": """<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="11" cy="11" r="7" stroke="currentColor" stroke-width="2"/>
        <path d="M16 16L21 21" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
    </svg>""",

    # Chevron Right (for breadcrumb)
    "chevron-right": """<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M9 6L15 12L9 18" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>""",

    # Chevron Down (for dropdown menus)
    "chevron-down": """<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M6 9L12 15L18 9" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>""",

    # Close icon
    "close": """<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M6 6L18 18M6 18L18 6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
    </svg>""",

    # Plus icon
    "plus": """<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M12 5V19M5 12H19" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
    </svg>""",

    # Windows Terminal
    "terminal": """<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect x="2" y="3" width="20" height="18" rx="3" fill="#1E1E1E"/>
        <path d="M6 8L10 12L6 16" stroke="#4EC9B0" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        <line x1="12" y1="16" x2="17" y2="16" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round"/>
    </svg>""",

    # File Generic
    "file": """<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M10 8C10 5.8 11.8 4 14 4H26L38 16V40C38 42.2 36.2 44 34 44H14C11.8 44 10 42.2 10 40V8Z" fill="#F3F3F3"/>
        <path d="M26 4V16H38" fill="#D8D8D8"/>
        <path d="M10 8C10 5.8 11.8 4 14 4H26L38 16V40C38 42.2 36.2 44 34 44H14C11.8 44 10 42.2 10 40V8Z" stroke="#B0B0B0" stroke-width="1.5"/>
    </svg>""",

    # File Text
    "file-text": """<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M10 8C10 5.8 11.8 4 14 4H26L38 16V40C38 42.2 36.2 44 34 44H14C11.8 44 10 42.2 10 40V8Z" fill="#F9F9F9"/>
        <path d="M26 4V16H38" fill="#D8D8D8"/>
        <line x1="16" y1="22" x2="32" y2="22" stroke="#0078D4" stroke-width="2" stroke-linecap="round"/>
        <line x1="16" y1="28" x2="32" y2="28" stroke="#8A8886" stroke-width="2" stroke-linecap="round"/>
        <line x1="16" y1="34" x2="26" y2="34" stroke="#8A8886" stroke-width="2" stroke-linecap="round"/>
        <path d="M10 8C10 5.8 11.8 4 14 4H26L38 16V40C38 42.2 36.2 44 34 44H14C11.8 44 10 42.2 10 40V8Z" stroke="#B0B0B0" stroke-width="1.5"/>
    </svg>""",

    # File Code
    "file-code": """<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M10 8C10 5.8 11.8 4 14 4H26L38 16V40C38 42.2 36.2 44 34 44H14C11.8 44 10 42.2 10 40V8Z" fill="#1E1E1E"/>
        <path d="M26 4V16H38" fill="#333333"/>
        <path d="M20 23L15 28L20 33" stroke="#60CDFF" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
        <path d="M28 23L33 28L28 33" stroke="#60CDFF" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
        <line x1="25" y1="22" x2="23" y2="34" stroke="#4EC9B0" stroke-width="2" stroke-linecap="round"/>
    </svg>""",

    # File Image
    "file-image": """<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M10 8C10 5.8 11.8 4 14 4H26L38 16V40C38 42.2 36.2 44 34 44H14C11.8 44 10 42.2 10 40V8Z" fill="#F9F9F9"/>
        <path d="M26 4V16H38" fill="#D8D8D8"/>
        <rect x="15" y="21" width="18" height="16" rx="2" fill="#107C41"/>
        <circle cx="19" cy="25" r="1.5" fill="#FFE082"/>
        <path d="M15 32L20 27L24 31L27 28L33 34H15V32Z" fill="#81C784"/>
        <path d="M10 8C10 5.8 11.8 4 14 4H26L38 16V40C38 42.2 36.2 44 34 44H14C11.8 44 10 42.2 10 40V8Z" stroke="#B0B0B0" stroke-width="1.5"/>
    </svg>""",

    # File Audio
    "file-audio": """<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M10 8C10 5.8 11.8 4 14 4H26L38 16V40C38 42.2 36.2 44 34 44H14C11.8 44 10 42.2 10 40V8Z" fill="#F9F9F9"/>
        <path d="M26 4V16H38" fill="#D8D8D8"/>
        <circle cx="24" cy="28" r="8" fill="#FF8C00"/>
        <path d="M23 24V29C23 29.8 22.3 30.5 21.5 30.5C20.7 30.5 20 29.8 20 29C20 28.2 20.7 27.5 21.5 27.5C21.8 27.5 22.1 27.6 22.3 27.7V24L26 23V27.5C26 28.3 25.3 29 24.5 29C23.7 29 23 28.3 23 27.5V24Z" fill="white"/>
        <path d="M10 8C10 5.8 11.8 4 14 4H26L38 16V40C38 42.2 36.2 44 34 44H14C11.8 44 10 42.2 10 40V8Z" stroke="#B0B0B0" stroke-width="1.5"/>
    </svg>""",

    # File Video
    "file-video": """<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M10 8C10 5.8 11.8 4 14 4H26L38 16V40C38 42.2 36.2 44 34 44H14C11.8 44 10 42.2 10 40V8Z" fill="#F9F9F9"/>
        <path d="M26 4V16H38" fill="#D8D8D8"/>
        <rect x="15" y="22" width="18" height="14" rx="2" fill="#8764B8"/>
        <path d="M22 26L27 29L22 32V26Z" fill="white"/>
        <path d="M10 8C10 5.8 11.8 4 14 4H26L38 16V40C38 42.2 36.2 44 34 44H14C11.8 44 10 42.2 10 40V8Z" stroke="#B0B0B0" stroke-width="1.5"/>
    </svg>""",

    # File Archive
    "file-archive": """<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M10 8C10 5.8 11.8 4 14 4H26L38 16V40C38 42.2 36.2 44 34 44H14C11.8 44 10 42.2 10 40V8Z" fill="#FCE8B2"/>
        <path d="M26 4V16H38" fill="#FBC02D"/>
        <rect x="22" y="16" width="4" height="2" fill="#5F6368"/>
        <rect x="22" y="20" width="4" height="2" fill="#5F6368"/>
        <rect x="22" y="24" width="4" height="2" fill="#5F6368"/>
        <rect x="21" y="28" width="6" height="8" rx="1" fill="#757575"/>
        <circle cx="24" cy="32" r="1.5" fill="#FFE082"/>
        <path d="M10 8C10 5.8 11.8 4 14 4H26L38 16V40C38 42.2 36.2 44 34 44H14C11.8 44 10 42.2 10 40V8Z" stroke="#F57F17" stroke-width="1.5"/>
    </svg>""",

    # File PDF
    "file-pdf": """<svg viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M10 8C10 5.8 11.8 4 14 4H26L38 16V40C38 42.2 36.2 44 34 44H14C11.8 44 10 42.2 10 40V8Z" fill="#FFF"/>
        <path d="M26 4V16H38" fill="#F44336"/>
        <rect x="13" y="24" width="22" height="12" rx="2" fill="#D32F2F"/>
        <text x="16" y="33" fill="white" font-family="sans-serif" font-weight="bold" font-size="8">PDF</text>
        <path d="M10 8C10 5.8 11.8 4 14 4H26L38 16V40C38 42.2 36.2 44 34 44H14C11.8 44 10 42.2 10 40V8Z" stroke="#D32F2F" stroke-width="1.5"/>
    </svg>""",

    # Properties
    "properties": """<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/>
        <line x1="12" y1="11" x2="12" y2="17" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
        <circle cx="12" cy="7.5" r="1" fill="currentColor"/>
    </svg>""",

    # Theme Moon / Sun
    "theme": """<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>""",

    # View Mode: Details
    "view-details": """<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect x="3" y="5" width="4" height="3" rx="0.5" fill="currentColor"/>
        <line x1="9" y1="6.5" x2="21" y2="6.5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
        <rect x="3" y="10.5" width="4" height="3" rx="0.5" fill="currentColor"/>
        <line x1="9" y1="12" x2="21" y2="12" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
        <rect x="3" y="16" width="4" height="3" rx="0.5" fill="currentColor"/>
        <line x1="9" y1="17.5" x2="21" y2="17.5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
    </svg>""",

    # View Mode: Large Icons
    "view-large": """<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect x="3" y="3" width="7" height="7" rx="1.5" stroke="currentColor" stroke-width="2"/>
        <rect x="14" y="3" width="7" height="7" rx="1.5" stroke="currentColor" stroke-width="2"/>
        <rect x="3" y="14" width="7" height="7" rx="1.5" stroke="currentColor" stroke-width="2"/>
        <rect x="14" y="14" width="7" height="7" rx="1.5" stroke="currentColor" stroke-width="2"/>
    </svg>""",

    # View Mode: List
    "view-list": """<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <line x1="4" y1="6" x2="20" y2="6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
        <line x1="4" y1="12" x2="20" y2="12" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
        <line x1="4" y1="18" x2="20" y2="18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
    </svg>""",

    # View Mode: Tiles
    "view-tiles": """<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect x="3" y="4" width="8" height="6" rx="1" stroke="currentColor" stroke-width="2"/>
        <rect x="13" y="4" width="8" height="6" rx="1" stroke="currentColor" stroke-width="2"/>
        <rect x="3" y="14" width="8" height="6" rx="1" stroke="currentColor" stroke-width="2"/>
        <rect x="13" y="14" width="8" height="6" rx="1" stroke="currentColor" stroke-width="2"/>
    </svg>""",
}

_icon_cache = {}

def get_icon(name: str, color: str = None, size: int = 32) -> QIcon:
    """Return a QIcon for the given name with optional color replacement."""
    cache_key = (name, color, size)
    if cache_key in _icon_cache:
        return _icon_cache[cache_key]

    svg_str = SVGS.get(name, SVGS.get("file"))
    if color and "currentColor" in svg_str:
        svg_str = svg_str.replace("currentColor", color)
    elif "currentColor" in svg_str:
        svg_str = svg_str.replace("currentColor", "#FFFFFF")

    renderer = QSvgRenderer(QByteArray(svg_str.encode("utf-8")))
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)

    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    renderer.render(painter)
    painter.end()

    icon = QIcon(pixmap)
    _icon_cache[cache_key] = icon
    return icon

def get_pixmap(name: str, color: str = None, size: int = 32) -> QPixmap:
    """Return a QPixmap for the given icon name."""
    svg_str = SVGS.get(name, SVGS.get("file"))
    if color and "currentColor" in svg_str:
        svg_str = svg_str.replace("currentColor", color)
    elif "currentColor" in svg_str:
        svg_str = svg_str.replace("currentColor", "#FFFFFF")

    renderer = QSvgRenderer(QByteArray(svg_str.encode("utf-8")))
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)

    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    renderer.render(painter)
    painter.end()

    return pixmap
