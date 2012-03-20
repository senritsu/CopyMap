from org.bukkit.inventory import ItemStack
import org.bukkit as bukkit

def checkCubicForNearby(material, location, radius = 4):
    """

    checkCubicForNearby(material, location[, radius])

    Checks if at least one block of some material is found around a location

    material > org.bukkit.Material or int
    location > org.bukkit.Location
    radius > int, optional, defaults to 4 (ingame block interaction range)

    """
    # i holds the int id of the material to check against
    i = material.id if type(material) == bukkit.Material else material

    world = location.getWorld()

    # +1 to compensate for range excluding the last number
    radius = int(radius)+1
    # construct search coordinates starting at 'location' and then checking first positive and then negative offsets up to radius
    coordinates = range(radius)+range(-1,-radius,-1)
    x,y,z = map(int,map(round,(location.getX(),location.getY(),location.getZ())))
    x_range,y_range,z_range = [k+x for k in coordinates],[k+y for k in coordinates],[k+z for k in coordinates]

    # search
    for y in y_range:
        for x in x_range:
            for z in z_range:
                j = world.getBlockTypeIdAt(x,y,z)
                if i == j:
                    return True
    return False

@hook.enable
def onEnable():
  print "CopyMap v%s enabled"%info.getVersion()

@hook.disable
def onDisable():
  print "CopyMap v%s  disabled"%info.getVersion()

@hook.command("copymap", usage="/<command> (holding a map in hand)",
                desc="Craft a copy of the currently held map (requires nearby workbench and proper crafting materials)")
def copymap(sender, command, label, args):
    # return proper usage if player holds anything but a map in his hands
    if not sender.getItemInHand().getType() == bukkit.Material.MAP:
        return False

    inventory = sender.getInventory()
    # get amount of paper and compasses the player carries
    paper = sum([stack.getAmount() for stack in inventory.all(bukkit.Material.PAPER).values()])
    compass = sum([stack.getAmount() for stack in inventory.all(bukkit.Material.COMPASS).values()])

    # check if player is near a workbench
    if not checkCubicForNearby(bukkit.Material.WORKBENCH,sender.getLocation()):
        sender.sendMessage("You must be near a workbench to create a map")
    # check if player has enough materials to create a map
    elif paper < 8 or compass < 1:
        sender.sendMessage("Not enough materials to create a map")
    # create map copy
    else:
        # remove crafting materials from map
        paper = ItemStack(bukkit.Material.PAPER,8)
        compass = ItemStack(bukkit.Material.COMPASS,1)
        inventory.removeItem([paper,compass])
        # clone map and drop it at player location
        sender.getWorld().dropItemNaturally(sender.getLocation(),sender.getItemInHand().clone())
    return True

