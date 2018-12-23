//
//  VisualViewController.swift
//  safetracker
//
//  Created by Rohit Dsouza on 20/12/18.
//  Copyright © 2018 Rohit Dsouza. All rights reserved.
//

import UIKit
import Charts

class VisualViewController: UIViewController {
    
    @IBOutlet weak var crimeChartView: PieChartView!
    
    var crimes: [String]!
    var avgdist: [Double] = []
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view.
        
        crimes = ["Murder", "Theft", "Harrasment", "Robbery"]
        avgdist = [20.0, 40.0, 30.0, 10.0]
        
        createChart(dataPoints: crimes, values: avgdist)
        
    }
    

    func createChart(dataPoints: [String], values: [Double]){
        
        // 2. generate chart data entries
        
        var entries = [PieChartDataEntry]()
        for (index, value) in values.enumerated() {
            let entry = PieChartDataEntry()
            entry.y = value
            entry.label = dataPoints[index]
            entries.append( entry)
        }
        
        let set = PieChartDataSet( values: entries, label: "Pie Chart")
        var colors: [UIColor] = []
        
        for _ in 0..<values.count {
            let red = Double(arc4random_uniform(256))
            let green = Double(arc4random_uniform(256))
            let blue = Double(arc4random_uniform(256))
            let color = UIColor(red: CGFloat(red/255), green: CGFloat(green/255), blue: CGFloat(blue/255), alpha: 1)
            colors.append(color)
        }
        set.colors = colors
        let data = PieChartData(dataSet: set)
        crimeChartView.data = data
        crimeChartView.noDataText = "No data available"
        // user interaction
        crimeChartView  .isUserInteractionEnabled = true
        
        //let d = Description()
        //d.text = "iOSCharts.io"
        //chart.chartDescription = d
        crimeChartView.centerText = "Crimes"
        crimeChartView.holeRadiusPercent = 0.2
        crimeChartView.transparentCircleColor = UIColor.clear
    
    }
    
    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destination.
        // Pass the selected object to the new view controller.
    }
    */

}
