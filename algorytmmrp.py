import math

class Product:
    def __init__(self, name, lead_time=1, on_hand=0, safety_stock=0, batch_size=1):
        self.name = name
        self.lead_time = lead_time  
        self.on_hand = on_hand      
        self.safety_stock = safety_stock
        self.batch_size = batch_size
        self.components = []        

    def add_component(self, component, quantity_needed):
        self.components.append((component, quantity_needed))

    def calculate_mrp(self, gross_requirements, periods):
        print(f"\n--- Planowanie MRP dla: {self.name} ---")
        
        projected_available = self.on_hand
        net_requirements = [0] * periods
        planned_order_receipts = [0] * periods
        planned_order_releases = [0] * periods

        for t in range(periods):
            needed = gross_requirements[t] - projected_available + self.safety_stock
            
            if needed > 0:
                orders_to_make = math.ceil(needed / self.batch_size) * self.batch_size
                planned_order_receipts[t] = orders_to_make
                net_requirements[t] = needed
            else:
                net_requirements[t] = 0

            projected_available += planned_order_receipts[t] - gross_requirements[t]
            
            release_t = t - self.lead_time
            if release_t >= 0:
                planned_order_releases[release_t] = planned_order_receipts[t]

        self.print_table(periods, gross_requirements, net_requirements, planned_order_releases)

        for component, ratio in self.components:
            comp_gross = [qty * ratio for qty in planned_order_releases]
            component.calculate_mrp(comp_gross, periods)

    def print_table(self, periods, gross, net, release):
        header = "Okres:          |" + "".join([f"{i+1:4}" for i in range(periods)])
        g_row =  "Zapotrzeb. Brutto|" + "".join([f"{g:4}" for g in gross])
        n_row =  "Zapotrzeb. Netto |" + "".join([f"{n:4}" for n in net])
        r_row =  "Planowane wydanie|" + "".join([f"{r:4}" for r in release])
        print(header)
        print("-" * len(header))
        print(g_row)
        print(n_row)
        print(r_row)

rower = Product("Rower", lead_time=2, on_hand=10, safety_stock=5, batch_size=1)
kolo = Product("Koło", lead_time=1, on_hand=5, safety_stock=2, batch_size=10)

rower.add_component(kolo, 2)

demand = [0, 0, 0, 0, 0, 0, 0, 20, 0, 10]

rower.calculate_mrp(demand, 10)