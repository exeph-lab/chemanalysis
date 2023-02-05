## Questions (23-01-18, LT)

a) Kaip gerai skenavimo metu (per visus žingsnius) išlaikoma hipotezė, kad "ranka" pasirinktos atomų grupės sudaro plokštumas? Kurios struktūros turi mažiausius nuokrypius nuo visų taškų konkrečioje plokštumoje, kurios -- didžiausius ir apie kokio dydžio nuokrypius kalbama?

b) Ar yra skirtumų įskaitant vandenilio atomus į plokštumos "fitą", ar ne? Šiuo atveju spėčiau, kad nebus, bet BODIPY darinių variantai protonų vietoje turės šonines grupes, kurios jau gali būti traktuojamos atskirai, tad norisi pasitikrinti, ar dabar protonai tvarkingai "gula" į anglies karkaso plokštumas.

## Follow-up (23-01-31, LT)

3. Aš pamenu, kad reakcijos koordinatės šuolis skenavimo metu yra vienas, bet tavo "angles between planes" grafikuose pereinamieji efektai trunka ~6-8 žingsnius tarp dviejų šuoliukų. Ar gali užmesti akį, kas ten vyksta ir konkrečiai -- kokia yra antro šuoliuko prigimtis?
4. Tame pačiame grafike kažkuris iš fenilo-sparno kampų iki barjero formaliai yra neigiamas (ta pačia kryptimi skaičiuojant).
5. Kad BODIPY po truputį plokštėja (žalia kreivė, 0-20 iter.) artėjant prie barjero, man netikėta. Čia tikrovė ar priklauso nuo sparno plokštumos apibrėžimo?
6. RMSE yra labai grubus įrankis, jis dažnai tepasako "taip/ne". Tie patys grafikai su maksimaliu ir viduriniu (median) atitinkamų atomų atstumu nuo rastos plokštumos leistų geriau įvertinti tiek paklaidos dydį, tiek kas labiausiai iššoka. Tiesa, jei dabar reikšmės pateiktos/sunormuotos vienam atomui, tai median atstumų kreivės turėtų būti labai panašios.
7. Aš galiu racionalizuoti, kas nutinka C21 atomui už barjero "distances of atoms" grafikuose, bet kad H23/25 kažkur važiuoja, molekulei simetrizuojantis ties S1R padėtimi, that's weird. Ar H28/30 irgi daro tą patį, t. y. jie "nuleipsta" anglies karkaso atžvilgiu?

## Response (23-02-02, LT)

> 3. Aš pamenu, kad reakcijos koordinatės šuolis skenavimo metu yra vienas, bet tavo "angles between planes" grafikuose pereinamieji efektai trunka ~6-8 žingsnius tarp dviejų šuoliukų. Ar gali užmesti akį, kas ten vyksta ir konkrečiai -- kokia yra antro šuoliuko prigimtis?

Per Gaussview vaizdas būtent taip ir atrodo - ties maždaug 25 ir 35 konformacija įvyksta staigūs šuoliai, o BODIPY labiausiai išsilenkia tarp šitų šuolių.

> 4. Tame pačiame grafike kažkuris iš fenilo-sparno kampų iki barjero formaliai yra neigiamas (ta pačia kryptimi skaičiuojant).

Visi kampai lyg ir teigiami bei maždaug > 5 laipsniai.
Čia gal verta pridėt komentarą, kad aš skaičiuoju kampą tarp plokštumų normalių vektorių, bet vėliau kampus k didesnius negu 90 laipsnių persuku į 180 - k, t. y. visada pasilieku mažesnį kampą tarp plokštumų. Kitu atveju grafiko proporcijos stipriai išsikreipia, nes fittin'ant plokštumas ties 25 ir 26 konformacijom šoninių sparnų normalių vektoriai pakeičia kryptį ir šuolis atrodo labai didelis, nors iš tiesų tėra tik apie 10 laipsnių.

> 5. Kad BODIPY po truputį plokštėja (žalia kreivė, 0-20 iter.) artėjant prie barjero, man netikėta. Čia tikrovė ar priklauso nuo sparno plokštumos apibrėžimo?

Lyg ir tikrovė. Vizualiai BODIPY dalis iš pradžių truputį išsilenkus į vieną pusę ir iki 25 konformacijos artėja prie plokščios padėties. Tada ties 26 konformacija staiga gan stipriai išsilenkia į priešingą pusę. Tai taip pat paaiškina, kodėl abiejų sparnų normalių vektoriai pakeičia kryptį.

> 7. Aš galiu racionalizuoti, kas nutinka C21 atomui už barjero "distances of atoms" grafikuose, bet kad H23/25 kažkur važiuoja, molekulei simetrizuojantis ties S1R padėtimi, that's weird. Ar H28/30 irgi daro tą patį, t. y. jie "nuleipsta" anglies karkaso atžvilgiu?

Anglies karkaso plokštumos atžvilgiu labiausiai nuvažiuoja H23 ir H30, t. y. H atomai arčiausiai BODIPY, o mažiausiai H31, t. y. H priešingoj pusėj nei BODIPY.

---

## Report

I didn't implement PCA or any other method to find planes automatically yet, but I did the fitting error analysis with and without H atoms when fitting. [Here](https://github.com/exeph-lab/chemanalysis/blob/main/rg_scripts/bdp-phenyl-meoh-modelling-dynamics.ipynb)'s the source code.

And here are some graphs I generated. It seems like the hydrogen atoms effect the results at $10^{-2}$ angstrom order.

### Angles between planes

<details>
<summary><b>Graphs</b></summary>


![image](https://user-images.githubusercontent.com/59236770/216161666-faa29b19-bea7-41e1-a847-0da9db962d0b.png)
![image](https://user-images.githubusercontent.com/59236770/216161706-7d41d639-9865-431f-888b-bca139f11543.png)

</details>

### Root mean square error of plane fitting

<details>
<summary><b>Graphs</b></summary>

![image](https://user-images.githubusercontent.com/59236770/216161732-2969e814-9954-4c57-8304-24f1cadc2e76.png)
![image](https://user-images.githubusercontent.com/59236770/216161772-9772194f-4e56-4dea-9319-59de8d1c8c59.png)

</details>

### Distances of hydrogen atoms to the approximate plane of phenyl cycle

<details>
<summary><b>Graphs</b></summary>

![image](https://user-images.githubusercontent.com/59236770/216175784-f431a13e-3760-45b7-a782-deb00d26315c.png)
![image](https://user-images.githubusercontent.com/59236770/216175803-954a0f96-5d15-4b0b-8d05-450f87660030.png)

</details>

The maximum distances of atoms to the fitted plane are roughly 2-3 times bigger than RMSE, but the qualitative picture is very similar. Even the farthest outliers from the plane are still distance < $10^{-1}$ angstroms away.

### Median distance of atoms to the fitted plane

<details>
<summary><b>Graphs</b></summary>

![image](https://user-images.githubusercontent.com/59236770/216162430-ce74eceb-8eae-40c0-92e9-4a8bba9f64ef.png)
![image](https://user-images.githubusercontent.com/59236770/216162460-ab9e2343-4d30-4f01-a7d9-6a5f995bb21d.png)

</details>

### Maximum distance of atoms to the fitted plane

<details>
<summary><b>Graphs</b></summary>

![image](https://user-images.githubusercontent.com/59236770/216162650-88994116-745d-4b89-80f8-1f61d0ce494e.png)
![image](https://user-images.githubusercontent.com/59236770/216162616-a2b2b361-147d-452e-b89e-e01a851e35b7.png)

</details>

---

