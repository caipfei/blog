function is_leap(year){
      if (year%4 == 0 && year%100 != 0 || year%400 == 0)
      {
        return 1
      }else{
        return 0
      }
    }
    var now = new Date()
    var year = now.getFullYear()
    var month = now.getMonth()
    var day = now.getDate()
    var week = now.getDay()
    var first_day = new Date(year,month,1).getDay()
    
    var months = new Array(31,28+is_leap(year),31,30,31,30,31,31,30,31,30,31)
    var tr_num = Math.ceil((first_day+months[month])/7)
   
    document.write('<table id="calendar"><caption>'+ year+'年'+(month+1)+'月'+'</caption>')
    document.write('<tr id="t_header"><th>日</th><th>一</th><th>二</th><th>三</th><th>四</th><th>五</th><th>六</th></tr>')
    for (var i=0;i<tr_num ;i++ )
    {
      document.write('<tr >')
      for (var j=0;j<7 ;j++ )
      {
        var ind = i*7 + j
        var date = ind-first_day+1
        if (date<=0)
        {
          date = months[month-1] + ind -first_day +1
        }
        else if (date>months[month])
        {
          date = date - months[month]
        }
        else{
          date = ind-first_day+1
        }
        date == day? document.write('<td bgcolor="red">'+date+'</td>') : document.write('<td>'+ date +'</td>')
      }
      document.write('</tr>')
    }

    document.write('</table>')