import sys, os
class Constants():

    styles = {
        "default" :
        { 
            "bandWidgetActive": "{background-color:lightblue;border-radius: 10px;}",
            "bandWidgetInactive": "{background-color:silver;border-radius: 10px;}"
        },
        "dark_mode":
        {
            "bandWidgetActive": "{background-color:#01344f;border-radius: 10px;}",
            "bandWidgetInactive": "{background-color:#333;border-radius: 10px;}"
        }
    }

    ctcss_tones = [
        "67.0", "69.3", "71.9", "74.4", "77.0", "79.7", "82.5", "85.4", "88.5", 
        "91.5", "94.8", "97.4", "100.0", "103.5", "107.2", "110.9", "114.8", 
        "118.8", "123.0", "127.3", "131.8", "136.5", "141.3", "146.2", "151.4", 
        "156.7", "162.2", "167.9", "173.8", "179.9", "186.2", "192.8", "203.5", 
        "210.7", "218.1", "225.7", "233.6", "241.8", "250.3"
    ]

    dcs_tones = [
        "023", "025", "026", "031", "032", "036", "043", "047", "051", "053", "054", 
        "065", "071", "072", "073", "074", "114", "115", "116", "122", "125", "131", 
        "132", "134", "143", "145", "152", "155", "156", "162", "165", "172", "174", 
        "205", "212", "223", "225", "226", "243", "244", "245", "246", "251", "252", 
        "255", "261", "263", "265", "266", "271", "274", "306", "311", "315", "325", 
        "331", "332", "343", "346", "351", "356", "364", "365", "371", "411", "412", 
        "413", "423", "431", "432", "445", "446", "452", "454", "455", "462", "464", 
        "465", "466", "503", "506", "516", "523", "526", "532", "546", "565", "606", 
        "612", "624", "627", "631", "632", "654", "662", "664", "703", "712", "723", 
        "731", "732", "734", "743", "754"
    ]

    gps_sentences = ['$GPRMC', '$GPGGA']

    def getProgramDir():
        return os.path.join(os.path.expanduser('~'), 'D75 CAT Control')
    
    def getBaseDir() -> str:
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            if os.path.basename(sys.argv[0]) == "d75_cat_control.py":
                base_path = os.path.dirname(os.path.realpath(sys.argv[0]))
            else:
                base_path = "."

        return base_path
    
    def getFilePath(file):
        return os.path.join(Constants.getBaseDir(), file)
    