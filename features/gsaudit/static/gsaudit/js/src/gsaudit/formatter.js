


gsaudit.Formatter = function() {
    
    var self = {}
    self.data = {
        values: [],
        distribution: [],
        avg_text: null
    }
    
    
    self.init = function(values) {
        $.each(values, function(index, value) {
            var intval = parseInt(value);
            self.data.ints.push(intval)
            sum += intval
            self.datadistribution[intval + 2]++
        })
        
        var avg = sum / ts.length
        if (avg < -1.7) {
            self.data.avg_text = '--'
        } else if (avg < -1.3) {
            self.data.avg_text = '--/-'
        } else if (avg < -0.7) {
            self.data.avg_text = '-'
        } else if (avg < -0.3) {
            self.data.avg_text = '-/o'
        } else if (avg < 0.3) {
            self.data.avg_text = 'o'
        } else if (avg < 0.7) {
            self.data.avg_text = '0/+'
        } else if (avg < 1.3) {
            self.data.avg_text = '+'
        } else if (avg < 1.7) {
            self.data.avg_text = '+/++'
        } else if (avg < 5) {
            self.data.avg_text = '++'
        }
        return self
    }        
          
    self.get_values = function() {
        return self.data.values
    }
    
    self.get_distribution = function() {
        return self.data.distribution
    }
    
    self.get_avg_text = function() {
        return self.data.avg_text
    }
    
    
    return self
}
