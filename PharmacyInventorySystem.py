import time

class Medicine:
    def __init__(self, medID, medName, medType, quantity, price):
        self.id = medID
        self.name = medName
        self.type = medType
        self.quantity = quantity
        self.price = price

    def display(self):
        print(f"ID: {self.id} | {self.name:12} | Type: {self.type:10} | "
              f"Price: ${self.price:5.2f} | Stock: {self.quantity}")

class hashTable:
    def __init__(self, capacity=10):
        self.capacity = capacity
        self.table = [None] * capacity
        self.size = 0

    def hashKey(self, key):
        return hash(key) % self.capacity

    def insert(self, key, value):
        index = self.hashKey(key)
        location = index
        while self.table[index] is not None:
            if self.table[index][0] == key:
                self.table[index] = (key, value)
                return
            index = (index + 1) % self.capacity
            if index == location:
                raise Exception("Hash Table is full")
        self.table[index] = (key, value)
        self.size += 1

    def search(self, key):
        index = self.hashKey(key)
        location = index
        while self.table[index] is not None:
            if self.table[index][0] == key:
                return self.table[index][1]
            index = (index + 1) % self.capacity
            if index == location:
                break
        return None

    def delete(self, key):
        index = self.hashKey(key)
        location = index
        while self.table[index] is not None:
            if self.table[index][0] == key:
                self.table[index] = None
                self.size -= 1
                return True
            index = (index + 1) % self.capacity
            if index == location:
                break
        return False

    def displayMedicines(self):
        result = []
        for slot in self.table:
            if slot is not None:
                result.append(slot[1])
        return result

    def __len__(self):
        return self.size

class PharmacySystem:
    def __init__(self):
        self.database = hashTable(capacity=10)

    def displayMedicines(self):
        if len(self.database) == 0:
            print("No medicine records in Pharmacy Inventory System.")
            return
        print("\n--- Medicine Records ----\n")
        for med in self.database.displayMedicines():
            med.display()
        print()

    def searchMedicine(self, medicineID):
        return self.database.search(medicineID)

    def addMedicine(self, medicine):
        self.database.insert(medicine.id, medicine)    # FIXED: use medicine.id
        print(f"Medicine {medicine.id} is added into Pharmacy Inventory System records.")

    def deleteMedicines(self, medicineID):
        if self.database.delete(medicineID):
            print(f"Medicine {medicineID} is deleted from record.")
        else:
            print(f"Unable to find medicine {medicineID}.")

def pharmacyMenu():
    print("\n===== Pharmacy Inventory System =====")
    print("1. Display all medicines")
    print("2. Search medicines by ID")
    print("3. Add medicine records")
    print("4. Delete medicine records")
    print("5. Exit")

def performanceComparison():
    print("\n" + "=" * 70)
    print("PERFORMANCE COMPARISON: Hash Table (linear probing) vs. Array (linear search)")
    print("=" * 70)

    # Create 10 sample medicines (same as in your inventory but more)
    medicines = []
    for i in range(1, 11):
        medicines.append(Medicine(i, f"Medicine_{i}", "tablet", 100, 10.0))

    # --- Insert into HASH TABLE (your own hashTable class) ---
    ht = hashTable(capacity=20)   # capacity larger than number of items to avoid full table
    for med in medicines:
        ht.insert(med.id, med)

    # --- Insert into ARRAY (Python list) ---
    array = medicines[:]   # copy

    # Keys to search: 5 existing (1,3,5,7,9) and 5 non-existing (100,200,300,400,500)
    existing_keys = [1, 3, 5, 7, 9]
    non_existing_keys = [100, 200, 300, 400, 500]
    all_keys = existing_keys + non_existing_keys

    repetitions = 10000   # number of times to repeat the entire set of searches

    # ---------- Measure Hash Table search time ----------
    start_ht = time.perf_counter()
    for _ in range(repetitions):
        for key in all_keys:
            _ = ht.search(key)   # returns Medicine or None
    end_ht = time.perf_counter()
    ht_time = (end_ht - start_ht) * 1000   # milliseconds

    # ---------- Measure Array (linear) search time ----------
    def array_search(arr, key):
        for med in arr:
            if med.id == key:
                return med
        return None

    start_arr = time.perf_counter()
    for _ in range(repetitions):
        for key in all_keys:
            _ = array_search(array, key)
    end_arr = time.perf_counter()
    arr_time = (end_arr - start_arr) * 1000

    # ---------- Results ----------
    total_searches = repetitions * len(all_keys)
    print(f"\nTotal searches performed: {total_searches:,} ( {repetitions} repetitions × {len(all_keys)} keys )")
    print(f"\nHash Table (linear probing) total time: {ht_time:.2f} ms")
    print(f"Array (linear search)           total time: {arr_time:.2f} ms")
    print(f"\n▶ Hash Table is {arr_time / ht_time:.2f} times faster than Array.\n")

def main():
    # Create an instance of PharmacySystem (not just the class)
    system = PharmacySystem()

    # Insert sample records
    sample_meds = [
        Medicine(101, "Panadol", "tablet", 100, 10.00),
        Medicine(102, "Cough Syrup", "syrup", 80, 15.50)
    ]
    for med in sample_meds:
        system.addMedicine(med)

    print("Welcome to Pharmacy Inventory System\n")

    while True:
        pharmacyMenu()
        try:
            choice = int(input("Enter choice: "))
            if choice == 1:
                system.displayMedicines()
            elif choice == 2:
                searchID = int(input("Enter medicine ID to search: "))
                med = system.searchMedicine(searchID)
                if med:
                    med.display()
                else:
                    print("Medicine not found.")
            elif choice == 3:
                print("\nPlease insert the medicine information below:")
                medID = int(input("Medicine ID: "))
                medName = input("Name: ")
                medType = input("Type (tablet, syrup, supplement): ")
                quantity = int(input("Quantity: "))
                price = float(input("Price: "))
                new_med = Medicine(medID, medName, medType, quantity, price)
                system.addMedicine(new_med)
            elif choice == 4:
                deleteID = int(input("Enter medicine ID to delete: "))
                system.deleteMedicines(deleteID)
            elif choice == 5:
                print("Exiting System. Thank you for using!")
                break
            else:
                print("Invalid input. Please enter 1-5.\n")
        except ValueError:
            print("Error: Invalid input. Please enter numbers only.\n")
        except Exception as e:
            print(f"Unexpected error: {e}\n")

    performanceComparison()

if __name__ == "__main__":
    main()