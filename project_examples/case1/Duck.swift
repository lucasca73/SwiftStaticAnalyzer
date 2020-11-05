class Other {
    var some: String = "Hi There!"
}

class Duck: Animal, OtherAnimals {
    var hi: String = "Quack!"

    func helloWorld() {
        print(self.hi)
    }

    func sayOther(other: Other) {
        print(other.some)
    }
}

class OtherAnimals {

}

class Animal {

}