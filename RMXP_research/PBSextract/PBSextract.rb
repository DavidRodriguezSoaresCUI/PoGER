################################################################################
# Save data to PBS files
################################################################################

# Notes:
# - PBTypes is generated at compile-time because its content depends on content
#   from 'PBS/types.txt' (see Compiler :1198->:1222)
#   > It contains functions PBTypes.getName(id) and constants PBTypes.getCount
#     and PBTypes.maxValue.
# - PBAbilities is generated at compile-time because its content depends on
#   content from 'PBS/abilities.txt' (see Compiler :1335->:1343)
#   > It contains functions PBAbilities.getName(id) and constants 
#     PBAbilities.getCount and PBAbilities.maxValue.
# - PBItems is generated at compile-time because its content depends on
#   content from 'PBS/items.txt' (see Compiler :1564->:1570)
#   > It contains functions PBAbilities.getName(id), PBItems.getNamePlural(id)
#     and constants PBAbilities.getCount and PBAbilities.maxValue.
# - PBTrainers is generated at compile-time because its content depends on
#   content from 'PBS/trainertypes.txt' (see Compiler :2496->:2505)
#   > It contains function PBAbilities.getName(id) and constants 
#     PBAbilities.getCount and PBAbilities.maxValue.
# - module MakeshiftConsts (Editor_Utilities :157->:188) TODO
# - Editor_Utilities has hardcoded data, useful as fallback (:192->:240) TODO

# Functions used :
# - getConstantName from Compiler :691
# - PBTypes.getName from Compiler :1202
# - PBTypes.isPseudoType? from PBTypes_Extra :15
# - PBTypes.getEffectiveness from PBTypes_Extra :23
# - pbGetMessage from Intl_Messages :719
# - pbGetAbilityConst from Editor_Utilities :242
# - readItemList from Compiler :1510


def writeBOM( f )
  # UTF-8 BOM
  f.write(0xEF.chr)
  f.write(0xBB.chr)
  f.write(0xBF.chr)
end


def csvquotePlus( s )
  res=csvquote(s)
  if !res.include?('"')
   res=sprintf('"%s"', res)
  end
  return res
end

# inverse of pbCompileTypes from Compiler :1111
def SaveTypes(savedir)
  # Save 'types'
     
  
  File.open(savedir+"/types.txt","wb"){|f|
    # UTF-8 BOM
    writeBOM( f )
    
    typesNbr=(PBTypes.maxValue rescue 20)
    for i in 0..typesNbr
       # For each type (by index), get name (readable and internal) ..
       name=PBTypes.getName(i) rescue nil
       #next if !name || name==""
       
       # Search in PBTypes constant table for entry with given index
       # pbGetTypeConst is a hardcoded fallback from Editor_Utilities :192
       internalName=getConstantName(PBTypes,i) rescue pbGetTypeConst(i)
       
       # Obtain other informations on types
       pseudoType=(PBTypes.isPseudoType?(i) rescue isConst?(i,PBTypes,QMARKS))
       specialType=(PBTypes.isSpecialType?(i) rescue pbIsOldSpecialType?(i))
       
       # Obtain weaknesses/resistances/immunities
       weaknesses=[]  # value 4
       resistances=[] # value 1
       immunities=[]  # value 0
       for j in 0..(PBTypes.maxValue rescue 20)
         cname=getConstantName(PBTypes,j) rescue pbGetTypeConst(j)
         next if !cname || cname==""
         eff=PBTypes.getEffectiveness(j,i)
         weaknesses.push(cname) if eff==4
         resistances.push(cname) if eff==1
         immunities.push(cname) if eff==0
       end
       
       # We don't want unneeded newlines
       lastType=(i==typesNbr)
       
       # Write to file
       f.write(sprintf("[%d]\r\n",i))
       f.write(sprintf("Name=%s\r\n",name))
       f.write(sprintf("InternalName=%s\r\n",internalName))
       f.write("IsPseudoType=true\r\n") if pseudoType
       f.write("IsSpecialType=true\r\n") if specialType
       f.write("Weaknesses="+weaknesses.join(",")+"\r\n") if weaknesses.length>0
       f.write("Resistances="+resistances.join(",")+"\r\n") if resistances.length>0
       if immunities.length>0
         f.write("Immunities="+immunities.join(",")+"\r\n") if !lastType
         f.write("Immunities="+immunities.join(",")) if lastType
       end
       f.write("\r\n") if !lastType
    end
  }
end


# abilities.txt record structure :
# id, internalName, readableName, description
# notes : id is a number, description is double-quoted text
# inverse of pbCompileAbilities from Compiler :1321
def SaveAbilities(savedir)
  # Save 'abilities'
  
  File.open(savedir+"/abilities.txt","wb"){|f|
     # UTF-8 BOM
     writeBOM( f )
       
     # Write entries for each ability
     abilityNbr=(PBAbilities.maxValue rescue PBAbilities.getCount-1 rescue pbGetMessageCount(MessageTypes::Abilities)-1)
     for i in 1..abilityNbr
       # For each type (by index), get name (readable and internal) ..
       internalName=getConstantName(PBAbilities,i) rescue pbGetAbilityConst(i)
       next if !internalName || internalName==""
       name=pbGetMessage(MessageTypes::Abilities,i)
       next if !name || name==""
       # Obtain description
       description=pbGetMessage(MessageTypes::AbilityDescs,i)
       description=csvquotePlus(description)
       
       # We don't want unneeded newlines
       lastAbility=(i==abilityNbr)
       
       # Write to file
       f.write(sprintf("%d,%s,%s,%s",
          i,
          csvquote(internalName),
          csvquote(name),
          description
       ))
       f.write("\r\n") if !lastAbility
     end
  }
end


# items.txt record structure :
# id, internalName, itemNameSingular, itemNamePlural, itemPocket, itemPrice,
# itemDescritption, itemUse, itemBattleUse, itemType, itemMachine
# Notes : 
# - itemMachine is a move ID (optional filed, used for TM/HM items)
# inverse of pbCompileItems from Compiler :1528
def SaveItems(savedir)
  # Save 'items'
  
  # First load data
  # items.dat record structure (see PItem_Items :4->:13) :
  # id, itemNameSingular, itemNamePlural, itemPocket, itemPrice,
  # itemDescritption, itemUse, itemBattleUse, itemType, itemMachine
  itemData=readItemList("Data/items.dat") rescue nil
  return if !itemData || itemData.length==0
  
  File.open(savedir+"/items.txt","wb"){|f|
     # UTF-8 BOM
     writeBOM( f )
     
     itemsNbr=itemData.length
     for i in 0...itemsNbr
       next if !itemData[i]
       
       # For each type (by index), data record ..
       data=itemData[i]
       # Obtain infos
       internalName=getConstantName(PBItems,i) rescue sprintf("ITEM%03d",i)
       next if !internalName || internalName=="" || data[0]==0
       #machine=""
       if data[ITEMMACHINE]>0
         machine=getConstantName(PBMoves,data[ITEMMACHINE]) rescue pbGetMoveConst(data[ITEMMACHINE]) rescue ""
       end
       # False postive check
       if machine!="" && !(internalName.include?('TM') || internalName.include?('HM'))
         machine=""
       end
       
       # We don't want unneeded newlines
       lastItem=(i==itemsNbr-1)
       
       f.write(sprintf("%d,%s,%s,%s,%d,%d,%s,%d,%d,%d,%s",
          data[ITEMID],
          csvquote(internalName),
          csvquote(data[ITEMNAME]),
          csvquote(data[ITEMPLURAL]),
          data[ITEMPOCKET],
          data[ITEMPRICE],
          csvquotePlus(data[ITEMDESC]),
          data[ITEMUSE],
          data[ITEMBATTLEUSE],
          data[ITEMTYPE],
          csvquote(machine)
       ))
       f.write("\r\n") if !lastItem
     end
 }
end


# tm.txt isa file structured in sections, each section having :
# - an internal Name
# - a list of pokemon (internal Names)
# Note :
# - Because the compiler implementation doesn't keep original move order, it's
#   not possible to recover original formatting, but its information can be.
# inverse of pbCompileMachines from Compiler :2375
def SaveMachines(savedir)
  # Save 'tm'
  
  # First load data
  # tm.dat record structure :
  # WordArray of species, indexed by move
  machines=load_data("Data/tm.dat") rescue nil
  
  
  return if !machines
  File.open(savedir+"/tm.txt","wb"){|f|
     # UTF-8 BOM
     writeBOM( f )
     
     machineNbr=machines.length
     for i in 1...machineNbr
       Graphics.update if i%50==0
       next if !machines[i]
         
       # For each machine (by index) obtain name ..
       movename=getConstantName(PBMoves,i) rescue pbGetMoveConst(i) rescue nil
       next if !movename || movename==""
       
       # .. and species being able to learn them
       learnableSpecies=machines[i]
       learnableSpeciesNbr=learnableSpecies.length
       x=[]
       for j in 0...learnableSpeciesNbr
         speciesname=getConstantName(PBSpecies,learnableSpecies[j]) rescue pbGetSpeciesConst(learnableSpecies[j]) rescue nil
         next if !speciesname || speciesname==""
         x.push(speciesname)
       end
       
       # We don't want unneeded newlines
       lastMachine=(i==machineNbr)
       
       f.write(sprintf("[%s]\r\n",movename))
       f.write(x.join(","))
       f.write("\r\n") if !lastMachine
     end
  }
end


# trainertypes.txt record structure (from wiki) :
# id, internalName, readableName, baseMoney, BGM, VictoryME, IntroME, gender, 
# skillLevel, Skillcodes
# Notes : 
# - BGM=BackGround Music, ME=Music Effect
# - BGM, VictoryME, IntroME and Skillcodes are left unused
# - It isn't clear if Skillcodes were ever implemented
# - If skillLevel isn't set, it will take the same value as baseMoney, therefore
#   original formatting MAY be lost, but it isn't a problem since it's just an
#   implicit-to-explicit value conversion.
# taken from Compiler :2436
def pbSaveTrainerTypes(savedir)
  # Save 'trainertypes'
  
  # First load data
  # trainertypes.dat record structure (see ) :
  # 
  trainertypes = load_data("Data/trainertypes.dat") rescue nil
  return if !trainertypes
  
  File.open(savedir+"/trainertypes.txt","wb"){|f|
    # UTF-8 BOM
    writeBOM( f )
    
    f.write("\# See the documentation on the wiki to learn how to edit this file.\r\n")
    f.write("\#-------------------------------\r\n")
    
    trainertypesNbr=trainertypes.length
    for i in 0...trainertypesNbr
      next if !trainertypes[i]
      
      record = trainertypes[i]
      cnst = getConstantName(PBTrainers,record[0]) rescue next
       
      # We don't want unneeded newlines
      lastTT=(i==trainertypesNbr)
      
      f.write(sprintf("%d,%s,%s,%d,%s,%s,%s,%s,%s,%s",
         record[0],
         csvquote(cnst),
         csvquote(record[2]),
         record[3],
         csvquote(record[4]),
         csvquote(record[5]),
         csvquote(record[6]),
         (record[7]) ? ["Male","Female","Mixed"][record[7]] : "Mixed",
         record[8]!=record[3] ? record[8] : "",
         record[9]
      ))
      f.write("\r\n") if !lastTT
    end
  }
end


def EventCommandID_toString(code)
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
    when 41
      return "Change tile"
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


def TransferPlayer_toString( parameters )
  direction=""
  case parameters[4]
    when 0
      direction="Keep"
    when 2
      direction="Down"
    when 4
      direction="Left"
    when 6
      direction="Right"
    when 8
      direction="Up"
    else
      direction=sprintf("Unexpected: %d", parameters[4])
  end
      
  return sprintf("Transfer: Map=%d, coord=(%d,%d), direction=%s\r\n",
                  parameters[1],
                  parameters[2],
                  parameters[3],
                  direction)
end




# with help from https://pastebin.com/kAtvPg3Y for Table class
def SaveMaps(savedir)
  #PokemonMapFactory
  for id in 31...35
    game_map=Game_Map.new
    game_map.setup(id) rescue next
    rpg_map=game_map.map
    datatable=game_map.data
    
    mapinfos=pbLoadRxData("Data/MapInfos")[id]
    
    File.open( sprintf("%s/Map%03d.txt", savedir, id),"wb"){|f|
      # UTF-8 BOM
      writeBOM( f )
      
      f.write("{\r\n")
      f.write("\t\"Table\": {\r\n")
      f.write(sprintf("\t\t\"xsize\": %d,\r\n", datatable.xsize))
      f.write(sprintf("\t\t\"ysize\": %d,\r\n", datatable.ysize))
      f.write(sprintf("\t\t\"zsize\": %d,\r\n", datatable.zsize))
      f.write("\t\t\"data\": [")
      
      
      for z in 0...datatable.zsize
        f.write("[")
        for y in 0...datatable.ysize
          f.write("[")
          for x in 0...datatable.xsize
            f.write(sprintf("%d", datatable[x,y,z]))
            f.write(", ") if x != datatable.xsize-1
          end
          f.write("]")
          f.write(", \r\n") if y != datatable.ysize-1
        end
        f.write("]")
        f.write(", \r\n\r\n") if z != datatable.zsize-1
      end
      f.write("]\r\n")
      f.write("},\r\n")
      f.write( sprintf("\t\"Name\" : \"%s\",\r\n", mapinfos.name) )
      f.write( sprintf("\t\"Tileset\" : \"%s\",\r\n", game_map.tileset_name) )
      f.write( sprintf("\t\"AutoTileset\" : \"%s\",\r\n", game_map.autotile_names) )
      f.write( sprintf("\t\"TerrainTags\" : \"%s\",\r\n", game_map.terrain_tags.class) )
      f.write( sprintf("\t\"BattleBack\" : \"%s\",\r\n", game_map.battleback_name.class) )
      f.write( sprintf("\t\"Autoplay_bgm\" : %s,\r\n", rpg_map.autoplay_bgm) )
      f.write( sprintf("\t\"BGM\" : \"%s\",\r\n", rpg_map.bgm.name) )
      f.write( sprintf("\t\"Autoplay_bgs\" : %s,\r\n", rpg_map.autoplay_bgs) )
      f.write( sprintf("\t\"BGS\" : \"%s\",\r\n", rpg_map.bgs.name) )
      f.write( sprintf("\t\"Encounter_list\" : [%s],\r\n", rpg_map.encounter_list.join(",")) )
      f.write( sprintf("\t\"Encounter_step\" : %d,\r\n", rpg_map.encounter_step) )
      f.write( sprintf("\t\"Events\" : %s,\r\n", rpg_map.events.class) )
      
      
      f.write("}\r\n")
      
      
      
      for game_event in game_map.events.values
        f.write( "\r\n\#============\r\nNewEvent\r\n\#============\r\n" )
        rpg_event=game_event.event
        # event is Game_Event
        # event.event is RPG::Event
        # event.list[i] are RPG::EventCommand
        
        f.write( sprintf("id: %d\r\n", rpg_event.id) )
        f.write( sprintf("name: %s\r\n", rpg_event.name) )
        f.write( sprintf("x: %d\r\n", rpg_event.x) )
        f.write( sprintf("y: %d\r\n", rpg_event.y) )
        f.write( sprintf("pages: %s\r\n", rpg_event.pages.class) ) # Array
        
        for page in rpg_event.pages
          f.write( "Page:\r\n" )
          #f.write( sprintf("page_graphic: %s\r\n", page.graphic.class) )
          f.write( sprintf("page_graphic_tile_id: %d\r\n", page.graphic.tile_id) )
          f.write( sprintf("page_graphic_character_name: %s\r\n", page.graphic.character_name) )
          f.write( sprintf("page_graphic_character_hue: %s\r\n", page.graphic.character_hue) )
          f.write( sprintf("page_graphic_direction: %d\r\n", page.graphic.direction) )
          f.write( sprintf("page_graphic_pattern: %d\r\n", page.graphic.pattern) )
          f.write( sprintf("page_graphic_opacity: %d\r\n", page.graphic.opacity) )
          for move in page.move_route.list
            f.write( sprintf("page_move_route_code: %d\r\n", move.code) )
            for parameter in move.parameters
              f.write( sprintf("page_move_route_parameters: %s\r\n", parameter.class) )
            end
          end
          f.write( sprintf("page_direction_fix: %s\r\n", page.direction_fix) )
          f.write( sprintf("page_always_on_top: %s\r\n", page.always_on_top) )
          
          for pl in page.list
            pl_code=EventCommandID_toString(pl.code)
            next if pl_code=="END"
            f.write( "Page_lvl2:\r\n" )
            f.write( sprintf("pl_code: %s\r\n", pl_code) )
            
            if pl_code=="Transfer Player"
              f.write( TransferPlayer_toString( pl.parameters ) )
              next
            end
            
            for param in pl.parameters
              if param.instance_of?(Fixnum)
                f.write( sprintf("pl_parameters: %d\r\n", param) ) if param!=-1
                next
              end
              if param.instance_of?(String)
                f.write( sprintf("pl_parameters: %s\r\n", param) )
                next
              end
              if param.instance_of?(RPG::MoveRoute)
                f.write( MoveRoute_toString(param) )
                next
              end
              if param.instance_of?(RPG::AudioFile)
                f.write( sprintf("Audio: \"%s\", vol=%d, pitch=%d\r\n", param.name, param.volume, param.pitch) )
                next
              end
              f.write( sprintf("pl_parameters???: %s\r\n", param.class) )
            end
          end
        end
        
      end
    }
  end
  
  
end



def pbSavePBS
  # Save data to human-readable files
  
  # First insure output folder exists
  dirPBS="PBSextract"
  Dir.mkdir(dirPBS) rescue Exception
  # Individual functions
  #SaveTypes(dirPBS)
  #SaveAbilities(dirPBS)
  #SaveItems(dirPBS)
  #SaveMachines(dirPBS)
  #pbSaveTrainerTypes(dirPBS)
  SaveMaps(dirPBS)
end
