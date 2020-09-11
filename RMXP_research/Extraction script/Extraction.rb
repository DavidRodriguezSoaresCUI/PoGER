$observer=[]
$observe=true
$codeConversion=true

$mapLocations = {}

$PEusedCodes=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,33,34,37,38,39,40,41,42,44,101,102,104,106,108,111,112,113,115,118,119,121,122,123,125,201,202,208,209,210,221,222,223,225,231,232,235,236,241,242,247,248,249,250,314,354,355,401,402,404,408,411,412,413,655]

def writeBOM( f )
  # UTF-8 BOM
  f.write(0xEF.chr)
  f.write(0xBB.chr)
  f.write(0xBF.chr)
end

def quote( s )
  return sprintf("\"%s\"", s)
end

def csvquotePlus( s )
  # extension to csvquote that works better for me
  # used for : quoting strings
  res=csvquote(s)
  if !res.include?('"')
   res=sprintf('"%s"', res)
  end
  return res
end

def EventCommandID_toString(code)
  # command ID (code) -> String
  case code
    when 0
      return "END"
    when 1
      return "Move Down"
    when 2
      return "Move Left"
    when 3
      return "Move Right"
    when 4
      return "Move Up"
    when 5
      return "Move SW"
    when 6
      return "Move SE"
    when 7
      return "Move NW"
    when 8
      return "Move NE"
    when 9
      return "Move at random"
    when 10
      return "Move Towards Player"
    when 11
      return "Move away from player"
    when 12
      return "1 step forward"
    when 13
      return "1 step backwards"
    when 14
      return "Jump X+,Y+"
    when 15
      return "Wait n seconds"
    when 16
      return "Turn down"
    when 17
      return "Turn left"
    when 18
      return "Turn right"
    when 19
      return "Turn Up"
    when 20
      return "Turn 90 Right"
    when 21
      return "Turn 90 Left"
    when 22
      return "Turn 180"
    when 23
      return "Turn 90 random"
    when 24
      return "Turn random"
    when 25
      return "Turn towards player"
    when 26
      return "Turn away from player"
    when 37 # Walk through walls
      return "WTW ON"
    when 38 # Walk through walls
      return "WTW OFF"
    when 39 # Always on top
      return "AOT ON"
    when 40 # Always on top
      return "AOT OFF"
    when 41
      return "Change tile"
    when 44
      return "Sound Effect"
    when 108
      return "Comment (particle effect?)"
    when 408
      return "Comment continued (particle effect?)"
    when 404
      return "NOP"
    when 412
      return "Branch END"
    when 509
      return "RPG::MoveCommand Object"
    when 655
      return "Script continued"
    when 101 # Show Text
      return "Show Text"
    when 102 # Show Choices
      return "Show Choices"
    when 401 # 101 extension for longer text
      return "Show More Text"
    when 402 # When [**]
      return "When [**]"
    when 403 # When Cancel
      return "When Cancel"
    when 103 # Input Number
      return "Input Number"
    when 104 # Change Text Options [not in VX]
      return "Change Text Options [not in VX]"
    when 105 # Button Input Processing [not in VX]
      return "Button Input Processing [not in VX]"
    when 106 # Wait [in VX: 230]
      return "Wait [in VX: 230]"
    when 111 # Conditional Branch
      return "Conditional Branch"
    when 411 # Else
      return "Else"
    when 112 # Loop
      return "Loop"
    when 413 # Repeat Above
      return "Repeat Above"
    when 113 # Break Loop
      return "Break Loop"
    when 115 # Exit Event Processing
      return "Exit Event Processing"
    when 116 # Erase Event [in VX: 214]
      return "Erase Event [in VX: 214]"
    when 117 # Call Common Event
      return "Call Common Event"
    when 118 # Label
      return "Label"
    when 119 # Jump to Label
      return "Jump to Label"
    when 121 # Control Switches
      return "Control Switches"
    when 122 # Control Variables
      return "Control Variables"
    when 123 # Control Self Switch
      return "Control Self Switch"
    when 124 # Control Timer
      return "Control Timer"
    when 125 # Change Gold
      return "Change Gold"
    when 126 # Change Items
      return "Change Items"
    when 127 # Change Weapons
      return "Change Weapons"
    when 128 # Change Armor
      return "Change Armor"
    when 129 # Change Party Member
      return "Change Party Member"
    when 131 # Change Windowskin [not in VX]
      return "Change Windowskin [not in VX]"
    when 132 # Change Battle BGM
      return "Change Battle BGM"
    when 133 # Change Battle End ME
      return "Change Battle End ME"
    when 134 # Change Save Access
      return "Change Save Access"
    when 135 # Change Menu Access
      return "Change Menu Access"
    when 136 # Change Encounter
      return "Change Encounter"
    when 201 # Transfer Player
      return "Transfer Player"
    when 202 # Set Event Location
      return "Set Event Location"
    when 203 # Scroll Map
      return "Scroll Map"
    when 204 # Change Map Settings
      return "Change Map Settings"
    when 205 # Change Fog Color Tone [in VX: Set Move Route]
      return "Change Fog Color Tone [in VX: Set Move Route]"
    when 206 # Change Fog Opacity [in VX: Get on/off Vehicle]
      return "Change Fog Opacity [in VX: Get on/off Vehicle]"
    when 207 # Show Animation [in VX: 212]
      return "Show Animation [in VX: 212]"
    when 208 # Change Transparent Flag [in VX: 211]
      return "Change Transparent Flag [in VX: 211]"
    when 209 # Set Move Route [in VX: 205]
      return "Set Move Route [in VX: 205]"
    when 210 # Wait for Move's Completion
      return "Wait for Move's Completion"
    when 221 # Prepare for Transition [Not in VX, now called Fadeout Screen]
      return "Prepare for Transition [Not in VX, now called Fadeout Screen]"
    when 222 # Execute Transition [Not in VX, now called Fadein Screen]
      return "Execute Transition [Not in VX, now called Fadein Screen]"
    when 223 # Change Screen Color Tone
      return "Change Screen Color Tone"
    when 224 # Screen Flash
      return "Screen Flash"
    when 225 # Screen Shake
      return "Screen Shake"
    when 231 # Show Picture
      return "Show Picture"
    when 232 # Move Picture
      return "Move Picture"
    when 233 # Rotate Picture
      return "Rotate Picture"
    when 234 # Change Picture Color Tone
      return "Change Picture Color Tone"
    when 235 # Erase Picture
      return "Erase Picture"
    when 236 # Set Weather Effects
      return "Set Weather Effects"
    when 241 # Play BGM
      return "Play BGM"
    when 242 # Fade Out BGM
      return "Fade Out BGM"
    when 245 # Play BGS
      return "Play BGS"
    when 246 # Fade Out BGS
      return "Fade Out BGS"
    when 247 # Memorize BGM/BGS [not in VX]
      return "Memorize BGM/BGS [not in VX]"
    when 248 # Restore BGM/BGS [not in VX]
      return "Restore BGM/BGS [not in VX]"
    when 249 # Play ME
      return "Play ME"
    when 250 # Play SE
      return "Play SE"
    when 251 # Stop SE
      return "Stop SE"
    when 301 # Battle Processing
      return "Battle Processing"
    when 601 # If Win
      return "If Win"
    when 602 # If Escape
      return "If Escape"
    when 603 # If Lose
      return "If Lose"
    when 302 # Shop Processing
      return "Shop Processing"
    when 303 # Name Input Processing
      return "Name Input Processing"
    when 311 # Change HP
      return "Change HP"
    when 312 # Change SP
      return "Change SP"
    when 313 # Change State
      return "Change State"
    when 314 # Recover All
      return "Recover All"
    when 315 # Change EXP
      return "Change EXP"
    when 316 # Change Level
      return "Change Level"
    when 317 # Change Parameters
      return "Change Parameters"
    when 318 # Change Skills
      return "Change Skills"
    when 319 # Change Equipment
      return "Change Equipment"
    when 320 # Change Actor Name
      return "Change Actor Name"
    when 321 # Change Actor Class
      return "Change Actor Class"
    when 322 # Change Actor Graphic
      return "Change Actor Graphic"
    when 331 # Change Enemy HP
      return "Change Enemy HP"
    when 332 # Change Enemy SP
      return "Change Enemy SP"
    when 333 # Change Enemy State
      return "Change Enemy State"
    when 334 # Enemy Recover All
      return "Enemy Recover All"
    when 335 # Enemy Appearance
      return "Enemy Appearance"
    when 336 # Enemy Transform
      return "Enemy Transform"
    when 337 # Show Battle Animation
      return "Show Battle Animation"
    when 338 # Deal Damage
      return "Deal Damage"
    when 339 # Force Action
      return "Force Action"
    when 340 # Abort Battle
      return "Abort Battle"
    when 351 # Call Menu Screen
      return "Call Menu Screen"
    when 352 # Call Save Screen
      return "Call Save Screen"
    when 353 # Game Over
      return "Game Over"
    when 354 # Return to Title Screen
      return "Return to Title Screen"
    when 355 # Script
      return "Script"
    else      # Other
      return sprintf("Undocumented code %d",code)
  end
end


def direction_toString( dir )
  case dir
    when 0
      return "Keep"
    when 2
      return "Down"
    when 4
      return "Left"
    when 6
      return "Right"
    when 8
      return "Up"
    else
      return sprintf("direction_toString:Undocumented: %d", dir)
  end
end


def TransferPlayer_toString( parameters )
      
  return sprintf("Transfer: Map=%d, coord=(%d,%d), direction=%s\r\n",
                  parameters[1],
                  parameters[2],
                  parameters[3],
                  direction_toString( parameters[4] ) )
end


def MoveRoute_toString( mc )
  s=""
  for movecommand in mc.list
    s+=sprintf("pl_parameters_movecommand_code: %s\r\n", EventCommandID_toString(movecommand.code))

    for param_lvl2 in movecommand.parameters
      s+=sprintf("pl_parameters_movecommand_parameters: %s\r\n", param_lvl2)
    end  
  end
  return s
end

def list_toString( list, escapeQuotes=false )
  lst=""
  first=true
  if !list || !(list.is_a? Array)
    return sprintf( "list_toString1: unsupported class %s", list.class )
  end
  
  list.each{ |el|
    
    if el.is_a? String
      tmp=el
      if escapeQuotes
        tmp=el.gsub(/\"/, '\\"')
      end
      lst.concat( (first) ? quote(tmp) : ", "+quote(tmp) )
    elsif el.is_a? Fixnum
      lst.concat( (first) ? el.to_s : ", "+el.to_s )
    elsif el.is_a? TrueClass
      lst.concat( (first) ? el.to_s : ", "+el.to_s )
    elsif el.is_a? FalseClass
      lst.concat( (first) ? el.to_s : ", "+el.to_s )
    elsif el.is_a? Array
      lst.concat( list_toString(el) )
    elsif el.is_a? Tone
      lst.concat( sprintf('{ "_class":"Tone", "RGBG":[%d, %d, %d, %d] }', el.red, el.green, el.blue, el.gray) )
    else
      tmp = el.toString() rescue sprintf( "list_toString2: unsupported class %s", el.class )
      lst.concat( (first) ? tmp : ", "+tmp )
    end
    #lst.concat( "@"+el.class.to_s )  
    first=false
  }
  case list.length
    when 0
      return "null"
    when 1
      return lst
    else
      return "[ "+lst+" ]"
  end
end

module RPG
  class Tileset
    
    def getName()
      return sprintf("%s",@name)
    end
    
    def table2str( t )
      n = t.xsize * t.ysize * t.zsize
      res="["
      for i in 0...(n-1)
        x = t[i]
        if x==nil
          $observer.push( sprintf('table2str: nil found at position %d', i) )
          next
        end
        if i>0
          res.concat(",")
        end
        res.concat( x.to_s )
      end
      res.concat("]")
      return res
    end
    
    def passages_new_format()
      n = @passages.xsize
      #$observer.push( sprintf("passages_new_format : %d %d %d ", @passages.xsize, @passages.ysize, @passages.zsize) )
      t = Table.new(n)
      for i in 0...(n-1)
        tmp = 0
        if @priorities[i] > 0
          tmp = 0b1000000
        end
        t[i] = @passages[i] + tmp
      end
      return t
      
    end
    
    def toString()
      #if @name!=@tileset_name
      #  $observer.push( sprintf("Warning : Tileset name mismatch : %s!=%s", @name, @tileset_name) )
      #end
      
      return sprintf("{ \"_class\":\"RPG::Tileset\", \"name\":\"%s\", \r\n\"passages\":%s, \r\n\"terrain_tags\":%s }",
        @tileset_name,
        self.table2str( self.passages_new_format() ),
        self.table2str(@terrain_tags) )
    end
  end
  
  class Event
    class Page
      class Condition
      
        def toString
          var_str=""
          if @variable_valid
            var_str=sprintf( '{ "id":%d, "val":%d }', @variable_id, @variable_value )
          else
            var_str="null"
          end
          return sprintf('{ "_class":"Page::Condition", "S1":%s, "S2":%s, "Var":%s, "SS":%s }',
                    (@switch1_valid) ? quote(@switch1_id.to_s) : "null",
                    (@switch2_valid) ? quote(@switch2_id.to_s) : "null",
                    var_str,
                    (@self_switch_valid) ? quote(@self_switch_ch) : "null")
        end
      end
      
      class Graphic
        
        def blend_type_toString
          case @blend_type
            when 0
              return "Normal"
            when 1
              return "Additive"
            when 2
              return "Substractive"
            else
              return sprintf("blend_type_toString:Undocumented %d", @blend_type)
            end
        end
        
        def toString
          
          #if @tile_id!=0
          #  $observer.push( sprintf("Page::Graphic:toString: tile_id has value not zero: %d", @tile_id) )
          #end
          
          return sprintf('{ "_class":"Page::Graphic", "tile_id":%d, "character_name":%s, "character_hue":%d, "direction":%s, "pattern":%d, "opacity":%d, "blend_type":%s }',
                    @tile_id,
                    quote( @character_name ),
                    @character_hue,
                    quote( direction_toString(@direction) ),
                    @pattern,
                    @opacity,
                    quote( blend_type_toString ) )
        end
      end
      
      def move_type_toString
        case @move_type
          when 0
            return '"Fixed"'
          when 1
            return '"Random"'
          when 2
            return '"Approach"'
          when 3
            return sprintf( "{ %s }", @move_route.toString() )
          else
            return sprintf("move_type_toString:Undocumented: %d", @move_type)
        end
      end
      
      def trigger_toString
        case @trigger
          when 0
            return "onPlayerAction"
          when 1
            return "onPlayerTouch"
          when 2
            return "onEventTouch"
          when 3
            return "onAutorun"
          else
            return sprintf("trigger_toString:Undocumented: %d", @trigger)
        end
      end
      
      def toString_h
        return sprintf("\"move\":%s,\r\n \"move_speed\":%d, \"move_frequency\":%d, \"walk_anime\":%s, \"step_anime\":%s, \"direction_fix\":%s, \"through\":%s, \"always_on_top\":%s, \"trigger\":%s",
            move_type_toString,
            move_speed,
            move_frequency,
            walk_anime,
            step_anime,
            direction_fix,
            through,
            always_on_top,
            quote(trigger_toString) )
      end
      
      def toString
        lst=""
        first=true
        @list.each{ |ec|
          if ec.code==0 || ec.code==509
            next
          end
          tmp=ec.toString()
          if tmp.is_a? String
            lst.concat( (first) ? tmp : ",\r\n "+tmp )
          else
            $observer.push( sprintf("Page:toString: expected String, got %s", tmp.class.name) )
            next
          end
          first=false
        }
        
        return sprintf("{ \"_class\":\"Page\", \"condition\": %s,\r\n \"graphic\": %s,\r\n \"list\": %s,\r\n %s }",
                  @condition.toString(),
                  @graphic.toString(),
                  (lst=="") ? "null" : "[ "+lst+" ]",
                  toString_h)
      end
    end
  end
  
  class Event
  
    def toString
      lst=""
      first=true
      k=0
      @pages.each { |el|
        if !(el.is_a? RPG::Event::Page)
          lst.concat( sprintf("Event.toString: class=%s,%s", el.class.name, k.class.name) )
          next
        end
        tmp='"'+k.to_s+'": '+el.toString
        lst.concat( (first) ? tmp : ",\r\n "+tmp )
        first=false
        k+=1
      }
      
      return sprintf('{ "_class":"Event", "id": %d, "name": %s, "x": %d, "y": %d, "pages": %s }',
                @id,
                quote( @name ),
                @x,
                @y,
                (lst=="") ? "null" : "{ "+lst+" }" )
    end
  end
  
  class EventCommand
    
    def toString
      unless $PEusedCodes.include? @code
        $observer.push( sprintf("code %d", @code) )
        $PEusedCodes << @code
      end
      
      if $codeConversion
        return sprintf('{ "_class":"EventCommand", "code": %d, "indent": %d, "parameters": %s }',
                  @code,
                  @indent,
                  list_toString(@parameters, true) )
      end
      if @code==111
        $observer.push( sprintf("Conditional code %d : %s.",@parameters[0], sprintf('{ "_class":"EventCommand", "code": %s, "indent": %d, "parameters": %s }',
                  quote( EventCommandID_toString(@code) ),
                  @indent,
                  list_toString(@parameters, true) ) ) )
      end
      if false#@code==209
        return sprintf('"code": %s, "indent": %d, "parameters": null',
                quote( EventCommandID_toString(@code) ),
                @indent )
      else
        return sprintf('{ "_class":"EventCommand", "code": %s, "indent": %d, "parameters": %s }',
                  quote( EventCommandID_toString(@code) ),
                  @indent,
                  list_toString(@parameters, true) )
      end
    end
  end
  
  class MoveRoute
    
    def toString
        lst=""
        first=true
        @list.each{ |mc|
          if mc.code==0
            next
          end
          el=mc.toString()
          lst.concat( (first) ? el : ",\r\n "+el )
          first=false
        }
      
        return sprintf('{ "_class":"MoveRoute", "repeat": %s, "skippable": %s, "list": %s }',
                  repeat,
                  skippable,
                  (lst=="") ? "null" : "[ "+lst+" ]" )
    end
  end
  
  class MoveCommand
    
    def toString
      unless $PEusedCodes.include? @code
        $observer.push( sprintf("code %d", @code) )
        $PEusedCodes << @code
      end
      
      if $codeConversion
        return sprintf('{ "_class":"MoveCommand", "code": %d, "parameters": %s }',
                @code,
                list_toString(@parameters) )
      end
      if @parameters.is_a? Array
        return sprintf('{ "_class":"MoveCommand", "code": %s, "parameters": %s }',
                quote( EventCommandID_toString(@code) ),
                list_toString(@parameters) )
      else
        return sprintf('{ "_class":"MoveCommand", "code": %s, "parameters": Unexpected %s }',
                quote( EventCommandID_toString(@code) ),
                @parameters.class )
      end
    end
  end
  
  class AudioFile
    
    def shortString
      return sprintf('%s,%d,%d',
              @name,
              @volume,
              @pitch )
    end
    
    def toString
      return sprintf('{ "_class":"AudioFile", "name":%s, "volume":%d, "pitch":%d }',
              quote(@name),
              @volume,
              @pitch )
    end
  end
end


# with help from https://pastebin.com/kAtvPg3Y for Table class
def SaveMaps()
  
  
  mapinfos=pbLoadRxData("Data/MapInfos")
  
  Dir.mkdir('Maps') rescue Exception
  
  for id in 1...999
    if id%10==0
      Graphics.update
      Win32API.SetWindowText(_INTL("Processing map {1}...",id))
    end
    
    if !File.file?(sprintf("Data/Map%03d.rxdata", id))
      next
    end
    
    game_map=Game_Map.new
    game_map.setup(id) rescue next
    
    $observer.push( sprintf("SaveMaps: map%d",id))
    
    # Extracting info from game_map
    game_events=game_map.events
    #map_display_x=game_map.display_x
    #map_display_y=game_map.display_y
    map_id=game_map.map_id
    rpg_map=load_data(sprintf("Data/Map%03d.rxdata", map_id) )
    
    # Extracting info from rpg_map
    tileset_id=rpg_map.tileset_id
    width=rpg_map.width
    height=rpg_map.height
    auto_bgm=rpg_map.autoplay_bgm
    bgm=rpg_map.bgm
    auto_bgs=rpg_map.autoplay_bgs
    #bgs=rpg_map.bgs
    #encounter_list=rpg_map.encounter_list
    #encounter_step=rpg_map.encounter_step
    map_table=rpg_map.data
    rpg_events=rpg_map.events
    
    xsize=map_table.xsize
    ysize=map_table.ysize
    zsize=map_table.zsize
    map_name=mapinfos[id].name
    parent_map_id=mapinfos[id].parent_id
    parent_map_name=mapinfos[parent_map_id].name rescue nil
    tileset = $data_tilesets[tileset_id]
    
    # This part is responsible for structuring maps according to their
    # parent-child tree
    this_map_location = "Maps/"
    parent_map_location = $mapLocations[parent_map_id]
    if parent_map_location.is_a? String
      this_map_location = parent_map_location.dup
    end
    this_map_location.concat( sprintf("%s/", map_name.gsub(' ','_').gsub('\\','').gsub('/','_')) )
    $mapLocations[map_id] = this_map_location
    #$observer.push( sprintf( "$mapLocations : %d=>'%s'", map_id, $mapLocations[map_id] ) )
    Dir.mkdir($mapLocations[map_id]) rescue Exception
    
    if zsize!=3
      $observer.push( sprintf("Unexpected zsize for map %d : %d", map_id, zsize) )
    end
    if xsize!=width
      $observer.push( sprintf("Unexpected xsize for map %d : %d!=%d", map_id, xsize, width) )
    end
    if ysize!=height
      $observer.push( sprintf("Unexpected ysize for map %d : %d!=%d", map_id, ysize, height) )
    end
    
    # Extracting info from tileset
    tileset_name=tileset.tileset_name
    autotile_names=tileset.autotile_names
    pan_name=tileset.panorama_name
    pan_hue=tileset.panorama_hue
    fog_name=tileset.fog_name
    fog_hue=tileset.fog_hue
    fog_opacity=tileset.fog_opacity
    fog_blend=tileset.fog_blend_type
    fog_zoom=tileset.fog_zoom
    fog_sx=tileset.fog_sx
    fog_sy=tileset.fog_sy
    battleback=tileset.battleback_name
    passages=tileset.passages
    priorities=tileset.priorities
    terrain_tags=tileset.terrain_tags
    
    if width!=xsize || height!=ysize || 3!=zsize
      $observer.push( sprintf("Unexpected dims : w=%d, h=%d, x=%d, y=%d, z=%d",
        width, height, xsize, ysize, zsize) )
    end
    
    file_name = sprintf( "%d_%s", id, map_name.gsub(' ','_').gsub('\\','').gsub('/','_') )
    File.open( sprintf("%s%s.json", $mapLocations[map_id], file_name ),"wb"){|f|
      # UTF-8 BOM
      writeBOM( f )
      
      f.write("{\r\n")
      f.write("\t\"_class\": \"Map\",\r\n")
      #f.write(sprintf("\t\"id\": %d,\r\n", map_id))
      #f.write(sprintf("\t\t\"map_display_x\": %d,\r\n", map_display_x))
      #f.write(sprintf("\t\t\"map_display_y\": %d,\r\n", map_display_y))
      f.write(sprintf("\t\"width\": %d,\r\n", width))
      f.write(sprintf("\t\"height\": %d,\r\n", height))
      #f.write(sprintf("\t\"xsize\": %d,\r\n", xsize))
      #f.write(sprintf("\t\"ysize\": %d,\r\n", ysize))
      #f.write(sprintf("\t\"zsize\": %d,\r\n", zsize))
      
      f.write( sprintf("\t\"name\" : \"%s\",\r\n", map_name.gsub("\\", "/")) )
      #f.write( sprintf("\t\t\"Parent\" : \"%s\",\r\n", parent_map_name) )
      f.write( sprintf("\t\"tileset\" : \"%s\",\r\n", tileset_name) )
      f.write( sprintf("\t\"autotiles\" : %s,\r\n", list_toString(autotile_names)) )
      f.write( sprintf("\t\"battleback\" : %s,\r\n", quote(battleback)) )
      f.write( sprintf("\t\"autoplay_bgm\" : %s,\r\n", auto_bgm) )
      f.write( sprintf("\t\"bgm\" : %s,\r\n", quote(bgm.shortString)) )
      #f.write( sprintf("\t\t\"Autoplay_bgs\" : %s,\r\n", auto_bgs) )
      #f.write( sprintf("\t\t\"BGS\" : %s,\r\n", quote(bgs.name)) )
      #f.write( sprintf("\t\t\"Encounter_list\" : [%s],\r\n", encounter_list.join(",")) )
      #f.write( sprintf("\t\t\"Encounter_step\" : %d,\r\n", encounter_step) )
      
      f.write("\t\"table\": [")
      for z in 0...zsize
        f.write("[")
        for y in 0...ysize
          f.write("[")
          for x in 0...xsize
            f.write(sprintf("%d", map_table[x,y,z]))
            f.write(", ") if x != xsize-1
          end
          f.write("]")
          f.write(", \r\n") if y != ysize-1
        end
        f.write("]")
        f.write(", \r\n\r\n") if z != zsize-1
      end
      f.write("]\r\n")
      f.write("}\r\n")
      
    }
    
    #$observer=[]
    File.open( sprintf("%s%d.events", $mapLocations[map_id], id),"wb"){|f|
      # UTF-8 BOM
      writeBOM( f )
      
      lst=""
      first=true
      
      rpg_events.each{ |k,rpg_event|
      
        if !(rpg_event.is_a? RPG::Event)
          $observer.push( sprintf("Unexpected event class : %s", rpg_event.class) )
        end
        if !(rpg_event.pages.is_a? Array)
          $observer.push( sprintf("Unexpected event.pages class : %s", rpg_event.pages.class) )
        end
        
        tmp=rpg_event.toString()
        f.write( sprintf("%s\r\n", (first) ? "[\r\n"+tmp : ",\r\n\r\n"+tmp ) )
        first=false
      }
      if first
        f.write( "[" )
      end
      f.write( "\r\n]" )
    }
    
    

  end
  
end

def SaveTilesets()
  d = 'Tileset_data'
  Dir.mkdir(d) rescue Exception

  if $data_tilesets.is_a? NilClass
    $observer.push("$data_tilesets nil")
    return
  end
  
  Win32API.SetWindowText(_INTL("Processing tilesets..."))
  
  $data_tilesets.each { |t|
    if !(t.is_a? RPG::Tileset)
      next
    end
    
    name = t.name.gsub(' ','_').gsub('\\','').gsub('/','_')
    if name==""
      $observer.push("SaveTilesets: Unnamed tileset found. Skipping..")
      next
    else
      $observer.push( sprintf("SaveTilesets: %s",t.name))
    end
    
    File.open( sprintf("%s/%s.json", d, name ), "wb"){|f|
      # UTF-8 BOM
      writeBOM( f )
      
      f.write( t.toString().gsub('RPG::Tileset','Tileset') )
    }
  }
end

def writeObserver()
  File.open( sprintf("Extraction.log"),"wb"){|f|
    # UTF-8 BOM
    writeBOM( f )
    if $observe
      for observation in $observer
        
        f.write(observation+"\r\n")
      end
    end
    #f.write( sprintf("$game_variables:%s", $game_variables.class) )
    #for item in $game_variables
    #  f.write( sprintf("game_var:%s", item.class) )
    #end
  }
end



def pbSaveAll()
  SaveMaps(); Graphics.update
  SaveTilesets(); Graphics.update
  writeObserver()
end

