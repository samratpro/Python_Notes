## 00. How to select path
```
https://chromewebstore.google.com/detail/selectorshub-xpath-helper/ndgimibanhlabgdgjcpbbndiehljcpfh
```
```
(//div[@id='idname'])[1]   //use this way is best case for single element
```
## 01. Find all element
```
//element_name        # example : //div , //p, //img
```
## 02. Find all element and select by index (1-to-targeted)
```
(//element_name)[1]   # example : (//div)[1] , (//p)[1]
```
## 03. Find all element and select by index (1-to-targeted)
```
(//element_name)[1]   # example : (//div)[1] , (//p)[1]
```
## 04. Find by arribute
```
(//element_name[@arribute_name="value"])[1]            # example : (//div[@class="name"])[1] , (//div[@title="name"])[1] etc
//element_name[normalize-space()='inner_text']         # example : //h2[normalize-space()='Product details']
```
## 05. Find by Text
```
text='Element Text Name"
//button[.='Post']   # if text is exist in child level element of selected element
```
## 06. Find by CSS Selector
```
htmltag.classname
htmltag#idname
.classname
#idname
#p[attribute type='attribute name']   # attribute type can be class id data_test etc
//a[contains(@class, 'name') and contains(@class, 'name') and contains(text(), 'text name')]"
```
## 07. Find next of selected element
```
//element//element                                                                  # example : //address//button
element[arribute_name='value']                                                      # example : span[data-anonymize='email']
(//element_name[@arribute_name="value"])[1]//element                                # example : (//div[@class="name"])[1])//li
((//element_name[@arribute_name="value"])[1]//element)[1]                           # example : ((//div[@class="name"])[1])/li)[1]
((//element_name[@arribute_name="value"])[1]//element[@arribute_name="value"])[1]   # example : ((//div[@class="name"])[1])//li[@id="name"])[1]
```
## 08. Loop logic
```
elements = selector_all('//any-xpath')
for e in elements:
    print(e.text())
# Or
i = 1
while i < n:
    print(select(f'(//path)[{str(i)}]'))
    i+=1
```
## 09. How to intertact JS click from browser devs
```
- from inspect element of targeted element
- right click > copy > copy js path
- insert copy in JS console (F12) and add .click() function and inter
```
