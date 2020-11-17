protocol FriendsProtocol {
    func askForHelp() -> Bool
    func wannaHangout() -> Bool
}

extension FriendsProtocol {
    func partyAllNight()
}

class FriendCircle<Friend: FriendsProtocol> {
    var people = [Friend]()

    func callForHelp() {
        for p in people {
            p.askForHelp()
        }
    }
}

class MySelf {
    var neighbors: FriendCircle<Neighbor>()
    var family: FriendCircle<Neighbor>()

    func callForHelp() {
        neighbors.callForHelp()
        family.callForHelp()
    }
}

class Neighbor: FriendsProtocol {
    func askForHelp() -> Bool {
        return false
    }

    func wannaHangout() -> Bool {
        return true
    }
}

class Family: FriendsProtocol {
    func askForHelp() -> Bool {
        return true
    }

    func wannaHangout() -> Bool {
        return false
    } 
}