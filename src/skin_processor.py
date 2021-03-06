import yaml_loader as yl


def dictobj(name, value):
    return {"name": str(name),
            "value": value
            }


class Skin:
    # Reference: https://taehui.ddns.net/bbs/board.php?bo_table=rtfm&wr_id=3
    #            (Korean)

    def __init__(self):
        # Initialize
        self.name = ""
        self.resource = ""
        self.luafile = ""

        self.frame = []
        self.framerate = []
        self.color = []
        self.render_order = []
        self.style = []
        self.drawing = []
        self.input_mode = []

    def importYAML(self, yamlfile):
        # Check type
        if not isinstance(yamlfile, yl.YAMLFile):
            raise TypeError

        # Load header
        self.name = yamlfile.file_name
        self.resource = yamlfile.header["zip"]
        self.luafile = yamlfile.header["lua"]

        # Load numbers of frames and framerates
        for value_name in yamlfile.frame:
            obj_name = value_name.replace('-', '_')
            if value_name.endswith("framerate"):
                obj_name = obj_name.replace('_framerate', '')
                self.framerate.append(dictobj(obj_name,
                                              yamlfile.frame[value_name]))
            elif value_name.endswith("frame"):
                obj_name = obj_name.replace('_frame', '')
                self.frame.append(dictobj(obj_name,
                                          yamlfile.frame[value_name]))

        # Load result rank color
        for value_name in yamlfile.paint:
            if value_name.startswith("quit-"):
                ranks = ('x', 'u', 's', 'a', 'b', 'c', 'd')
                rank_number = int(value_name.split('-')[-1])

                self.color.append(dictobj("rank_%s" % ranks[rank_number],
                                          yamlfile.paint[value_name]))

            else:
                self.color.append(dictobj(value_name.replace('-', '_'),
                                          yamlfile.paint[value_name]))

        # Load styles in playing (function)
        for value_name in yamlfile.function:
            # Render order(pipeline)
            if value_name == "pipeline":
                pipeline_str = str(yamlfile.function["pipeline"])
                for obj_num in pipeline_str.split(","):
                    self.render_order.append(int(obj_num))
                del pipeline_str

            # Key style number configure
            elif value_name.startswith("ui-drawing-"):
                img_num = int(value_name.split('-')[-1])
                input_num = str(yamlfile.function[value_name]).split(",")
                self.drawing.append({"num": img_num,
                                     "target": input_num})

            # Order key style by each Key modes
            elif value_name.startswith("ui-input-mode-"):
                mode_num = int(value_name.split('-')[-1])
                order_num = str(yamlfile.function[value_name]).split(",")
                self.input_mode.append({"mode": mode_num,
                                        "target": order_num})

    def exportYAML(self):
        # Header
        header = {"zip": self.resource, "lua": self.luafile}

        # Frames and framerates
        # Initialize for frames and framerates list
        frame = {}

        # Frames
        for eatch_object in self.frame:
            key_name = eatch_object["name"] + "-frame".replace('_', '-')
            frame[key_name] = eatch_object["value"]

        # Framerates
        for eatch_object in self.framerate:
            key_name = eatch_object["name"] + "-framerate".replace('_', '-')
            frame[key_name] = eatch_object["value"]

        # Paint
        # Initialize for paint list
        paint = {}

        # For debug
        print(header)
        print(frame)


# For test
if __name__ == '__main__':
    example_file_path = "Default.yaml"
    file_object = yl.YAMLFile()
    file_object.road(example_file_path)
    example_skin = Skin()
    example_skin.importYAML(file_object)

    # Debug Data
    print("Name:", example_skin.name)
    print("Resouse Zip:", example_skin.resource)
    print("Lua Script:", example_skin.luafile)
    print("")
    print("Frames of each objects")
    print(example_skin.frame)
    print("")
    print("Framerate of each objects")
    print(example_skin.framerate)
    print("")
    print("Color")
    print(example_skin.color)
    print("")
    print("Pipeline")
    print(example_skin.render_order)
    print("")
    print("Style")
    print(example_skin.style)
    print("")
    print("Drawing")
    print(example_skin.drawing)
    print("")
    print("Key Sets")
    print(example_skin.drawing)
    print("")
    print("")
    print("Exporting...")
    example_skin.exportYAML()
