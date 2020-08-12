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

=begin
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
=end

