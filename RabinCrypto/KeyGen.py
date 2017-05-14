from secrets import randbits

class KeyGen(object):
    """description of class"""
    
    small_primes = []
    
    def safe_random(this, a, b):
        modulus = b - a + 1
        ok = False
        bits, mv = 0, 1
        while mv < modulus:
            mv <<= 1
            bits += 1
        mav = (mv // modulus) * modulus
        while not ok:
            rv = randbits(bits+1)
            if rv < mav:
                rv %= modulus
                ok = True
        return a + rv

    def lower_bound(this, a, x, start=0, end=None):
        if end == None:
            end = len(a) - 1
        c = -1
        while end - start > 1:
            c = (start + end) >> 1
            if a[c] <= x:
                start = c
            else:
                end = c
        return start

    def prepare_small_primes(this):
        this.small_primes = [2, 3]
        last = 3
        while last < 65536:
            next = last
            ok = False
            while not ok:
                next += 2
                ok = True
                for p in this.small_primes:
                    if p * p > next:
                        break
                    else:
                        if not next % p:
                            ok = False
                            break
            this.small_primes.append(next)
            last = next

    def ensure_small_primes(this):
        if not len(this.small_primes):
            this.prepare_small_primes()

    def miller_rabin_test(this, n, k):
        this.ensure_small_primes()
        d = n - 1
        s = 0
        while not d & 1:
            d >>= 1
            s += 1
        for a in this.small_primes[:k]:
            composite = True
            ad = pow(a, d, n)
            if ad == 1:
                composite = False
            else:
                for r in range(s):
                    if ad == n - 1:
                        composite = False
                        break
                    ad = (ad * ad) % n
            if composite:
                return False
        return True

    def prime_up_to(this, n):
        this.ensure_small_primes()
        if n < 65536:
            return this.small_primes[this.lower_bound(this.small_primes, n)]
        if not n & 1:
            n -= 1
        ok = False
        while not ok:
            small_ok = False
            while not small_ok:
                small_ok = True
                for p in this.small_primes:
                    if not n % p:
                        small_ok = False
                        n -= 2
                        break
            ok = this.miller_rabin_test(n, 20)
            if not ok:
                n -= 2
        return n

    def random_prime(this, a, b):
        rv = this.safe_random(a, b)
        p = this.prime_up_to(rv)
        if p < a:
            p = this.prime_up_to(b + a - rv)
            if p < a:
                p = this.prime_up_to(b)
        return p

    def hexString(this, bits):
        listF = ['f'] * (bits // 4)
        return ''.join(listF)

    def keyGen(this, bits):
        max = int(this.hexString(bits), 16)
        min = max - int(this.hexString(bits - 4), 16)

        while True:
            priv_p = this.random_prime(min, max)
            priv_q = this.random_prime(min, max)        
            if priv_p % 4 != 3 or priv_q % 4 != 3: 
                continue
            if priv_p != priv_q: return (priv_p, priv_q)

